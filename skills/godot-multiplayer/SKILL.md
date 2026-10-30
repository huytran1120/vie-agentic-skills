---
name: godot-multiplayer
description: >
  Build networked games with Godot 4.7 high-level multiplayer: set up an
  ENetMultiplayerPeer server/client, define RPCs with the @rpc annotation
  (call via rpc()/rpc_id()), set per-node multiplayer authority, and replicate
  state with MultiplayerSpawner and MultiplayerSynchronizer. Use when adding
  multiplayer/networking to a Godot project, writing @rpc functions, or syncing
  player/world state across peers.
---

# Godot Multiplayer (4.x high-level)

Connect peers, call functions remotely with `@rpc`, assign authority, and replicate state
with `MultiplayerSpawner`/`MultiplayerSynchronizer`. Targets **Godot 4.7** (ENet). Treat
all client input as untrusted; keep the server authoritative.

## When to use

- Use when adding networked multiplayer: hosting/joining over ENet, calling RPCs,
  assigning per-node authority, or auto-spawning/syncing nodes across peers.

**When *not* to use:** local split-screen (no networking); raw TCP/UDP/WebSocket protocol
work (low-level `PacketPeer`); HTTP requests. For save/persistence → `save-systems`.

## Core workflow

1. **Create a peer** (`ENetMultiplayerPeer`), call `create_server(port, max)` or
   `create_client(ip, port)`, and assign it to `multiplayer.multiplayer_peer`. The
   server's unique ID is always `1`; clients get random positive IDs.
2. **Handle connection signals** on `multiplayer`: `peer_connected(id)`,
   `peer_disconnected(id)`, `connected_to_server`, `connection_failed`,
   `server_disconnected`.
3. **Define RPCs** with `@rpc(...)`. Call them on a `Callable` via `rpc()` (all peers) or
   `rpc_id(peer_id)` (one peer). Inside, `multiplayer.get_remote_sender_id()` tells you who
   sent it.
4. **Keep RPC signatures identical** on every peer that runs the script — Godot checksums
   all `@rpc` methods in a script; a mismatch prints errors that can name an unrelated RPC.
5. **Assign authority** per node with `set_multiplayer_authority(id)`; gate input/RPCs by
   `is_multiplayer_authority()`.
6. **Replicate state** with `MultiplayerSpawner` (auto-instances scenes on clients) and
   `MultiplayerSynchronizer` (auto-syncs selected properties).
7. **Validate on the server.** Don't trust client-reported positions/results.

## Patterns

### 1. Host or join (ENet)

```gdscript
const PORT := 7000
const MAX_PLAYERS := 8

func host() -> void:
    var peer := ENetMultiplayerPeer.new()
    var err := peer.create_server(PORT, MAX_PLAYERS)
    if err != OK:
        push_error("Cannot host: %s" % err); return
    multiplayer.multiplayer_peer = peer
    multiplayer.peer_connected.connect(_on_peer_connected)

func join(ip := "127.0.0.1") -> void:
    var peer := ENetMultiplayerPeer.new()
    peer.create_client(ip, PORT)
    multiplayer.multiplayer_peer = peer
    multiplayer.connected_to_server.connect(func(): print("connected"))

func leave() -> void:
    multiplayer.multiplayer_peer = OfflineMultiplayerPeer.new()
```

### 2. RPCs: client sends input to the server (any_peer, call_local)

This script sits on a player avatar whose authority is the owning client (Pattern 3), so
the server is *not* the node's authority. A server→clients RPC on such a node must be
`"any_peer"` and check that the sender is the server.

```gdscript
func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("fire") and is_multiplayer_authority():
        request_fire.rpc_id(1)          # send only to the server (id 1)

# Clients may call this; it runs on the server (and locally if server is a player).
@rpc("any_peer", "call_local", "reliable")
func request_fire() -> void:
    if not multiplayer.is_server():     # ignore copies relayed to other clients
        return
    var sender := multiplayer.get_remote_sender_id()
    if not _can_fire(sender):           # server-side validation
        return
    spawn_projectile.rpc(sender)        # tell everyone to spawn it

# "authority" here would make clients reject the server's call (the client is the
# authority), so accept any peer and keep only calls that come from the server.
@rpc("any_peer", "call_local", "reliable")
func spawn_projectile(owner_id: int) -> void:
    if multiplayer.get_remote_sender_id() != 1:
        return
    _do_spawn(owner_id)
```

### 3. Per-node authority (each player controls their own avatar)

```gdscript
extends CharacterBody2D

func _ready() -> void:
    # The node name is the owning peer's id; that peer is the authority.
    set_multiplayer_authority(name.to_int())

func _physics_process(delta: float) -> void:
    if not is_multiplayer_authority():
        return                          # only the owner reads input & moves
    velocity = Input.get_vector("left", "right", "up", "down") * 200.0
    move_and_slide()
```

### 4. MultiplayerSynchronizer config (editor + replication)

```gdscript
# Add a MultiplayerSynchronizer child; in its Replication editor add the properties to
# sync (e.g. position, velocity). Set "Sync"/"Spawn" flags per property. From code you
# can scope visibility:
@onready var sync: MultiplayerSynchronizer = $MultiplayerSynchronizer

func _ready() -> void:
    # Only replicate this node to a specific peer (e.g. private info). Per-peer visibility
    # matters only once public_visibility is off; by default every peer receives it.
    sync.public_visibility = false
    sync.set_visibility_for(target_peer_id, true)
```

## Pitfalls

- **RPC signature checksum.** Every `@rpc` method in a script must exist with the same
  declaration on both client and server builds — *even unused ones*. A mismatch causes
  errors that may point at the wrong function. Argument names/count are not checked, but
  the set of RPCs and their annotations are.
- **Default `@rpc` is `"authority"`.** Clients calling it are ignored unless you set
  `"any_peer"`. Use `"call_local"` so the host (also a player) runs it too.
- **`RPC 'x' is not allowed on node ... from: 1. Mode is "authority"`** → the server called
  an `"authority"` RPC on a node a client owns. "Authority" means the node's authority, not
  the server. Use `"any_peer"` plus a `get_remote_sender_id() == 1` check, or move
  server-driven RPCs to a server-owned node (e.g. a game manager).
- **NodePaths must match across peers.** RPC routing uses the node's path/name; spawn nodes
  with identical names on all peers (use `MultiplayerSpawner` or `add_child(node, true)` for
  readable, deterministic names).
- **Trusting the client.** Never let clients set authoritative state (health, position,
  hits) directly. Send *intent*, validate on the server, then broadcast results.
- **RPC on non-Node classes fails.** `@rpc` methods must be on `Node`-derived classes, not
  plain `Resource`/`RefCounted`.
- **RPCs don't serialize Objects/Callables.** Pass plain data (ints, strings, arrays,
  dictionaries, PackedArrays).
- **Forgetting to reset the peer.** To disconnect cleanly, set
  `multiplayer.multiplayer_peer = OfflineMultiplayerPeer.new()`.
- **Android needs INTERNET permission** in the export preset or all networking is blocked.

## References

- For `MultiplayerSpawner` setup, transfer modes/channels, `SceneMultiplayer`
  authentication (`auth_callback`/`complete_auth`), a lobby skeleton, and dedicated-server
  export notes, read `references/replication-and-rpc.md`.

## Related skills

- `godot-nodes-scenes` — instancing the scenes that get spawned/synced.
- `godot-signals-groups` — connection signals and event flow.
- `godot-export` — exporting a headless dedicated server build.


## VAS installation notes

Imported from gamedev-skills/awesome-gamedev-agent-skills at
`19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9`, Apache-2.0.
Copyright 2026 Abhishek Barali and the awesome-gamedev-agent-skills contributors.
The complete upstream LICENSE and NOTICE accompany this standalone skill.
Third-party notices, including the Go-Fonts license where provided, remain intact.
Only documented VAS naming, router-path adaptations and these notes differ;
supporting files and executable modes are preserved.

Use Copy Agent Prompt in the VAS catalog or `./vas install <canonical-id> --target <agent>`.
VAS uses its existing agent-folder mapping and CLI-compatible receipt. Installing
a skill only copies/links its payload; it never runs bundled Python/Luau/Go code,
installs engines, SDKs, packages, plugins or MCP servers, connects accounts,
generates assets through paid services, uploads builds or publishes a game.
Review code and request permission before installation, execution, downloads,
external services, private-data submission, purchases or publishing.

Respect the existing project's pinned engine/dependency versions. Baselines in
the upstream runbooks are snapshots, not claims about the newest release.
Actual use may need the matching engine, Go/.NET/Luau/Node toolchain, SDK,
hardware or platform account. create-game-assets' optional image helpers need
Pillow>=10,<14; no Pillow or other runtime dependency is installed automatically.
Generated Ebitengine projects fetch their own Go modules only with approval;
the bundled Go-Fonts notice does not change the license of this runbook.
Storefront publishing, signing credentials and paid asset generation are separate,
explicitly authorized actions. Missing prerequisites or failed commands are errors,
not evidence that a game works or has shipped.

Collection names performance-optimization and godot-export mean VAS canonical IDs
gamedev-performance-optimization and gamedev-godot-export respectively, not the
unrelated existing application-performance or Blender-export skills.
Other source skill names retain their canonical IDs and installed folder names.
Cross-skill composition recommendations do not imply that other independent
skills or external tools have been installed. Each specialized skill includes
its own complete local references, helpers and assets. For automatic selection
across the collection, the separately installable router includes all 77 original
specialized payloads as read-only companions under bundled/skills/, with
RUNBOOK.md filenames rather than additional auto-discovered SKILL.md files.
Read only the selected companion and its references on demand; never execute
its helpers automatically. Bundled companions are references, not extra catalog
records or separately registered agent skills. External engines, documentation,
SDKs, services and generated project's dependencies remain separate prerequisites.
