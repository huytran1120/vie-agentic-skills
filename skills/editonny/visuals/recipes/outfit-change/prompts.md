# Outfit Change prompts

Replace bracketed details with the actual subject and scene. Preserve the identity, framing, motion and lighting constraints. Request a cost estimate and obtain authorization before generation. Model settings, observed limitations and assembly steps are in [README.md](README.md).

## 1. Request parameters

```json
{"model": "kling_video_edit", "mode": "pro",
 "medias": [{"role": "video_references", "value": "<clip_media_id>"},
            {"role": "image_references", "value": "<optional_clothing_or_target_image>"}],
 "prompt": "...", "get_cost": true}
```

## 2. Clothing only

```
Change only the man's clothing: replace his [current clothing, e.g. light-blue t-shirt] with [new clothing, e.g. a tailored navy blue blazer over a white dress shirt with open collar, no tie]. Keep everything else exactly the same: his face, [glasses, beard, hair], hands, [wristwatch and bracelets], [the small microphone he is holding], the background room [and plant], lighting, framing, camera, and all body motion, hand gestures and lip movements.
```

## 3. Consistent target image

```
Edit this photo. Keep the same [man] with the exact same face, [glasses, beard, hair], pose, hands, [wristwatch, bracelets, ring] and the [small handheld microphone]. Change ONLY two things. (1) Clothing: replace the [blue t-shirt] with [a clean white doctor's lab coat with long sleeves and a classic notched lapel, worn open over a light blue button-up dress shirt, with a stethoscope around his neck]. No logos, no name tag, no embroidery, no text. (2) Background: replace the [living room and the plant] with [a modern, bright medical consulting room: white walls, light wood and white furniture, a desk with a computer monitor, an examination table with a paper roll, one framed anatomical poster, white cabinets, a small green plant]. Soft natural daylight coming from the [left], same camera height and perspective as the original phone video, background slightly soft. Photorealistic, natural skin tones, vertical 9:16.
```

## 4. Match clothing and environment to the target

```
Edit the video so that the man's clothing and the room match the reference image exactly: [the same white doctor's lab coat with classic lapel worn open over a light blue button-up shirt, the same stethoscope around his neck], and the same [bright medical consulting room background (white walls, white cabinets, framed anatomical poster, examination table, desk with monitor, plants, window daylight)]. Keep from the video exactly: his face, [glasses, beard, hair], hands, fingers, [wristwatch, bracelets, ring], the framing, static camera, and all motion, hand gestures and lip movements. No logos, no text.
```

## 5. Describe clothing and environment together

```
Change the man's clothing AND the room: he wears [a clean off-white long-sleeve dentist coat with a short mandarin band collar and a closed front zipper, no logo, no text]. The background is now [a bright, modern dental clinic office: a white and light-blue dental chair with an overhead dental lamp, white cabinets, a small sink, soft clinical daylight]. The lighting on him matches the new room. Keep his face, [glasses, beard, hair], hands, [microphone, watch and bracelets, light blue jeans], framing, and all motion and lip movements exactly the same.
```

## 6. Body transformation

```
Make the man's body EXTREMELY muscular, like a professional heavyweight bodybuilder on stage. The change must be dramatic and obvious at first glance: massive bulging biceps and triceps at least twice as thick as his current arms, huge round deltoids, very wide shoulders, flaring lats that make his torso a wide V shape, a big thick chest stretching the fabric, thick neck and trapezius, muscular veiny forearms. He wears [a plain solid black sleeveless stringer tank top (no logo)] that shows the huge bare arms and shoulders, and his [dark grey shorts]. Keep his head exactly the same size and identity: same face, [glasses, beard, hair] and skin tone. Keep the [wristwatch and bracelets, the small microphone he is holding], the background room [and plant], lighting, framing, camera, and all body motion, [the finger snap, the arm flexing gesture] and lip movements exactly the same.
```

## 7. Replace a green hand guide

```
Replace the bright green placeholder object (a green bar with two round ends, drawn over the man's [lower fist]) with a realistic [black rubber hexagonal dumbbell with a chrome handle], like the one in the reference image. The [dumbbell] sits exactly where the green object is, in the same position, angle and size in every frame: [the handle passes through his closed lower fist, his fingers wrap around the handle, and one hex weight head sticks out on each side of the fist]. It moves with that fist exactly like the green object does. No green must remain anywhere. Keep everything else exactly the same: the man, his [black tank top], face, [glasses, beard, hair], arms, [wristwatch], [the small grey furry microphone in his other hand near his mouth], the background room [sofa and plant], lighting, framing, camera, body motion and lip movements.
```

## 8. Environment only

```
Replace the bright green hexagon placeholder (drawn over the man's [lower fist]) with a realistic [black rubber hexagonal dumbbell with a chrome handle], held in that fist and seen END-ON. [The man stands in profile doing a classic palm-up biceps curl, so the dumbbell's handle points straight toward the camera: we see the flat hexagonal face of the near weight head facing the camera], in the same position and about the same size as the green hexagon, with his thumb and fingers firmly wrapped around the handle right behind it[, and the far weight head hidden behind his hand]. The grip must look natural and solid, the [dumbbell] follows that fist exactly in every frame [as the arm curls up and lowers down], with realistic lighting, contact shadows and motion blur. No green must remain anywhere. Keep everything else exactly the same: [list every feature that must remain unchanged].
```

## Request notes and clothing variations

After cost authorization, remove `get_cost` to submit generation. Resend a preset recommendation with its `declined_preset_id`. Clothing descriptions that worked included a black tuxedo with satin peak lapels and bow tie; navy blazer over an open-collar white shirt; sage button-up shirt; caramel crew-neck sweater over a blue shirt; white double-breasted chef jacket with black apron; and a plain black athletic tank. Adapt the subject's gender and clothing accurately.

For walking or joined clips, add: “Preserve the cuts between shots, and all body motion, walking and lip movements frame by frame from the very first frame.” For fixed framing, add: “Do not zoom, crop, shift or resize the person; static camera, identical framing.” Generate two target-image alternatives and let the owner choose before reusing one across blocks. Recreating the complete room can produce lighting consistent with the new environment.

The weaker “very muscular bodybuilder physique” wording produced only an athletic result. Check the intended publishing platform's current rules when planning appearance-based advertising. Clothing and a handheld object can be edited together when the object has a guide. Do not alter hair to simulate reversed gravity: this invented curls and failed identity review in the observed attempt.
