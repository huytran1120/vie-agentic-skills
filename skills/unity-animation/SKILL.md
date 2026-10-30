---
name: unity-animation
description: >
  Drive Unity 6.3 LTS character animation with Animator Controllers: states, transitions,
  parameters, blend trees, animation layers, and humanoid Avatar IK. Use when wiring an
  Animator, setting parameters from script (SetFloat/SetBool/SetTrigger), building blend
  trees, or when the user mentions Animator, Mecanim, state machine, blend tree, or .controller.
---

# Unity Animation (Animator / Mecanim)

Control animation state with Unity 6.3 LTS's `Animator` and Animator Controllers: parameters,
transitions, blend trees, layers, and humanoid IK. Targets **Unity 6.3 LTS (6000.3)**.

## When to use

- Use when connecting animation clips into a state machine, driving them from script via
  parameters, blending locomotion (idle→walk→run), layering an upper-body action over
  movement, or adding foot/hand IK on a humanoid rig.
- Use when the project has `*.controller` (Animator Controller) and `*.anim` assets, or a
  rigged model with an Avatar.

**When *not* to use:** simple non-skeletal value tweens (UI fades, position lerps) are better
done with a tween/coroutine — see `unity-csharp-scripting`. Timeline cutscenes are a separate
tool. 2D sprite frame animation also uses the Animator but with sprite keyframes.

## Core workflow

1. **Add an `Animator`** to the model and assign an Animator Controller; for a humanoid model,
   set its rig to **Humanoid** so it has an Avatar (enables retargeting and IK).
2. **Define parameters** on the controller — `Float` (Speed), `Bool` (IsGrounded), `Int`,
   `Trigger` (Jump) — and states with transitions whose *conditions* read those parameters.
3. **Set parameters from script**, never poke states directly: `SetFloat`, `SetBool`,
   `SetInteger`, `SetTrigger`. The state machine resolves transitions for you.
4. **Blend continuous motion with a Blend Tree** (one `Float` like Speed drives idle↔walk↔run)
   instead of many discrete states + transitions.
5. **Layer additive/override motion** (e.g. an upper-body "aim" layer with an Avatar Mask) and
   control its `layerWeight`.
6. **Verify** in the Animator window during Play mode — the live state highlights and parameter
   values update, so you can see exactly which transition fired (or didn't).

## Patterns

### 1. Drive locomotion + a one-shot action from script

```csharp
using UnityEngine;

[RequireComponent(typeof(Animator))]
public class CharacterAnim : MonoBehaviour
{
    private Animator _anim;
    // Cache parameter hashes — faster and typo-proof vs string lookups every frame.
    private static readonly int Speed     = Animator.StringToHash("Speed");
    private static readonly int IsGrounded= Animator.StringToHash("IsGrounded");
    private static readonly int Jump      = Animator.StringToHash("Jump");

    private void Awake() => _anim = GetComponent<Animator>();

    public void Tick(float planarSpeed, bool grounded)
    {
        _anim.SetFloat(Speed, planarSpeed);     // drives a 1D blend tree (idle/walk/run)
        _anim.SetBool(IsGrounded, grounded);    // gates a falling/landing transition
    }

    public void DoJump() => _anim.SetTrigger(Jump);  // fire-and-forget; auto-resets after use
}
```

### 2. Smooth a noisy input into a blend parameter

```csharp
// dampTime smooths Speed so the blend tree doesn't snap; great for analog sticks.
_anim.SetFloat(Speed, targetSpeed, 0.1f /* dampTime */, Time.deltaTime);
```

### 3. Play / cross-fade a state directly (bypassing parameter conditions)

```csharp
// Useful for hit reactions where you want an immediate, explicit transition.
_anim.CrossFade("Hit", 0.1f);                    // 0.1 = 10% of the state's length, not seconds
_anim.CrossFadeInFixedTime("Hit", 0.15f);        // duration in seconds
// Or jump instantly:  _anim.Play("Hit");
```

### 4. Wait until the current state finishes

```csharp
private System.Collections.IEnumerator AfterAttack()
{
    yield return null;                                 // let the Animator start the transition
    // During a transition the "current" state is the one being left; read the next one.
    var info = _anim.IsInTransition(0)
        ? _anim.GetNextAnimatorStateInfo(0)
        : _anim.GetCurrentAnimatorStateInfo(0);        // layer 0
    yield return new WaitForSeconds(info.length);      // seconds; approximate, varies in blend trees
    // ...follow-up logic
}
```

## Pitfalls

- **`SetTrigger` missed or "sticks"** — triggers are consumed by the next satisfied transition
  and auto-reset; if no transition consumes it, it can fire later unexpectedly. Use
  `ResetTrigger` to clear, or prefer a `Bool` when the condition is a sustained state.
- **String parameter typos fail silently** — a misspelled name just does nothing. Use
  `Animator.StringToHash` and cache the int hashes.
- **Transition feels laggy** — `Has Exit Time` makes the transition wait for the clip to reach
  a normalized time. Uncheck it for responsive, condition-driven transitions (jump, hit).
- **Character slides or won't move** — `Apply Root Motion` is on but your code also moves the
  transform (or vice versa). Decide: root motion *or* scripted movement, not both.
- **Upper-body layer overrides the whole body** — set the layer's Blend mode (Override vs
  Additive), assign an Avatar Mask, and tune `layerWeight` (0–1).
- **A cross-fade is much slower or faster than expected** — `CrossFade`'s duration is
  *normalized* to the state's length. Use `CrossFadeInFixedTime` to give the
  duration in seconds.
- **IK does nothing** — IK only applies inside `OnAnimatorIK`, requires "IK Pass" enabled on
  the layer, and needs a Humanoid Avatar.

## References

- For **blend trees** (1D vs 2D Freeform/Directional), **animation layers + Avatar Masks**,
  and **humanoid IK** (`OnAnimatorIK`, `SetIKPositionWeight`, `SetIKPosition`, look-at), read
  `references/blend-trees-and-ik.md`.
- Primary docs: Unity Manual "Animation" section and `ScriptReference/Animator`.

## Related skills

- `unity-csharp-scripting` — the MonoBehaviour and coroutine timing used above.
- `unity-physics` — moving the body that the animation visualises.
- `game-ai` — deciding *when* to play which animation state.


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
