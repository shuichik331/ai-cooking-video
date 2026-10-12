# Generation prompt drafts — confirmation request to ChatGPT

Claude Code has **not** edited `prompts.json`. Below are draft prompts for the multi-shot generation groups. Each one is built only from your original text:

- **Kept verbatim:** each cut's own sentence(s), and every `global_prompt` sentence except the recipe sentence.
- **Removed:** the single `global_prompt` sentence that caused the 4-shot montage in s01 test-01:
  > Chicken nanban cooked from raw chicken thigh through egg batter frying, sweet-sour nanban sauce, egg-onion tartar sauce, plating and tasting.
- **Added (production wrapper):**
  - shot-count contract and per-shot timing labels
  - identity / environment reference lines (only where needed)
  - audio line (natural cooking sounds, no music or speech)
  - exclusions (no other stages, inserts or text)

Please confirm or edit each draft. Open decisions are listed first.

## Open decisions (groups blocked until answered)
- **G05 / s17:** Image: bare fingers lower a flour-coated piece into the oil. prompts.json: 'battered chicken being carefully lowered into hot oil with tongs'. Utensil (and batter look) differ.
- **G06 / s19:** Image: bare fingers add pieces to the hot oil. prompts.json: 'Close hands adding the next chicken pieces with tongs'. Utensil differs (also a hand-safety concern).
- **G07 / s25:** Image: chopsticks lift a piece above the frying pan, no rack in frame. prompts.json: 'Tongs lifting fully cooked golden chicken onto wire rack'. Utensil and destination differ.
- **G20 / s70:** Image and prompt both show tomatoes, but no tomato appears in the plating sequence s48–s54 or in s67. Continuity question for the creative lead.

## Drafts

### G01 — prep: fridge to board (s02, s03, s04, s05; 6 s)

Original per-cut text (unchanged):
- `s02`: Over shoulder view, same man opening his refrigerator.
- `s03`: Close view of the same man taking out a tray of raw chicken thigh.
- `s04`: Top-down still life of chicken, eggs, onion, rice vinegar, soy sauce and seasonings on wooden counter.
- `s05`: Close hands placing raw chicken on wooden cutting board.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 4 shots in 6.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.50s, storyboard s02): Over shoulder view, same man opening his refrigerator. Shot 2 (1.50-3.00s, storyboard s03): Close view of the same man taking out a tray of raw chicken thigh. Shot 3 (3.00-4.50s, storyboard s04): Top-down still life of chicken, eggs, onion, rice vinegar, soy sauce and seasonings on wooden counter. Shot 4 (4.50-6.00s, storyboard s05): Close hands placing raw chicken on wooden cutting board. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Keep the room identical to the separate kitchen environment reference. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G02 — prep: cutting and seasoning (s06, s07, s08; 5 s)

Original per-cut text (unchanged):
- `s06`: Macro knife shot cutting boneless chicken thigh into bite-size pieces.
- `s07`: Macro of safely trimming connective tissue from raw chicken.
- `s08`: Same man sprinkling salt and pepper onto chicken pieces.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 3 shots in 5.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.67s, storyboard s06): Macro knife shot cutting boneless chicken thigh into bite-size pieces. Shot 2 (1.67-3.34s, storyboard s07): Macro of safely trimming connective tissue from raw chicken. Shot 3 (3.34-5.00s, storyboard s08): Same man sprinkling salt and pepper onto chicken pieces. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G03 — batter: egg and flour (s09, s10, s11; 5 s)

Original per-cut text (unchanged):
- `s09`: Macro hands cracking egg into transparent mixing bowl.
- `s10`: Chopsticks rapidly whisk golden egg in glass bowl.
- `s11`: Close still life of flour arranged on a shallow white dish.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 3 shots in 5.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.67s, storyboard s09): Macro hands cracking egg into transparent mixing bowl. Shot 2 (1.67-3.34s, storyboard s10): Chopsticks rapidly whisk golden egg in glass bowl. Shot 3 (3.34-5.00s, storyboard s11): Close still life of flour arranged on a shallow white dish. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G04 — batter: coating (s12, s13, s14; 5 s)

Original per-cut text (unchanged):
- `s12`: Close hands evenly coating raw chicken pieces with flour.
- `s13`: Chopsticks dipping flour-coated chicken into beaten egg.
- `s14`: Extreme macro of egg-coated raw chicken, glossy wet batter.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 3 shots in 5.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.67s, storyboard s12): Close hands evenly coating raw chicken pieces with flour. Shot 2 (1.67-3.34s, storyboard s13): Chopsticks dipping flour-coated chicken into beaten egg. Shot 3 (3.34-5.00s, storyboard s14): Extreme macro of egg-coated raw chicken, glossy wet batter. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G05 — fry: oil and first piece (s15, s16, s17, s18; 6 s)

Original per-cut text (unchanged):
- `s15`: Medium shot of same man pouring cooking oil into dark frying pan.
- `s16`: Macro close-up of chopsticks testing preheated frying oil.
- `s17`: Close shot of battered chicken being carefully lowered into hot oil with tongs.
- `s18`: Extreme macro bubbling golden oil around chicken.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 4 shots in 6.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.50s, storyboard s15): Medium shot of same man pouring cooking oil into dark frying pan. Shot 2 (1.50-3.00s, storyboard s16): Macro close-up of chopsticks testing preheated frying oil. Shot 3 (3.00-4.50s, storyboard s17): Close shot of battered chicken being carefully lowered into hot oil with tongs. Shot 4 (4.50-6.00s, storyboard s18): Extreme macro bubbling golden oil around chicken. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G06 — fry: more pieces (s19, s20, s21, s22; 6 s)

Original per-cut text (unchanged):
- `s19`: Close hands adding the next chicken pieces with tongs.
- `s20`: Top-down shot of several pieces of chicken frying in a pan.
- `s21`: Extreme macro of the golden egg-battered crust puffing and crisping.
- `s22`: Medium profile shot of same man watching pan attentively.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 4 shots in 6.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.50s, storyboard s19): Close hands adding the next chicken pieces with tongs. Shot 2 (1.50-3.00s, storyboard s20): Top-down shot of several pieces of chicken frying in a pan. Shot 3 (3.00-4.50s, storyboard s21): Extreme macro of the golden egg-battered crust puffing and crisping. Shot 4 (4.50-6.00s, storyboard s22): Medium profile shot of same man watching pan attentively. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G07 — fry: turning and lifting (s23, s24, s25; 5 s)

Original per-cut text (unchanged):
- `s23`: Chopsticks carefully turning a piece of frying chicken.
- `s24`: Macro of crispy batter gradually turning amber gold.
- `s25`: Tongs lifting fully cooked golden chicken onto wire rack.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 3 shots in 5.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.67s, storyboard s23): Chopsticks carefully turning a piece of frying chicken. Shot 2 (1.67-3.34s, storyboard s24): Macro of crispy batter gradually turning amber gold. Shot 3 (3.34-5.00s, storyboard s25): Tongs lifting fully cooked golden chicken onto wire rack. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G08 — fry: draining and second batch (s26, s27, s28; 5 s)

Original per-cut text (unchanged):
- `s26`: Macro oil droplets draining from chicken above a wire rack.
- `s27`: Close shot of remaining battered chicken frying in oil.
- `s28`: Hero close-up of cooked golden fried chicken cooling on wire rack.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 3 shots in 5.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.67s, storyboard s26): Macro oil droplets draining from chicken above a wire rack. Shot 2 (1.67-3.34s, storyboard s27): Close shot of remaining battered chicken frying in oil. Shot 3 (3.34-5.00s, storyboard s28): Hero close-up of cooked golden fried chicken cooling on wire rack. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G09 — sauce: pouring (s29, s30, s31; 5 s)

Original per-cut text (unchanged):
- `s29`: Same man pouring clear rice vinegar into small stainless saucepan.
- `s30`: Macro dark soy sauce streaming into saucepan.
- `s31`: Macro white granulated sugar added to sweet vinegar soy mixture.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 3 shots in 5.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.67s, storyboard s29): Same man pouring clear rice vinegar into small stainless saucepan. Shot 2 (1.67-3.34s, storyboard s30): Macro dark soy sauce streaming into saucepan. Shot 3 (3.34-5.00s, storyboard s31): Macro white granulated sugar added to sweet vinegar soy mixture. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G10 — sauce: heating (s32, s33, s34; 5 s)

Original per-cut text (unchanged):
- `s32`: Side shot of saucepan gently heating on stovetop.
- `s33`: Macro sweet-and-sour nanban sauce lightly simmering.
- `s34`: Macro glossy amber nanban sauce lifted with spoon.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 3 shots in 5.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.67s, storyboard s32): Side shot of saucepan gently heating on stovetop. Shot 2 (1.67-3.34s, storyboard s33): Macro sweet-and-sour nanban sauce lightly simmering. Shot 3 (3.34-5.00s, storyboard s34): Macro glossy amber nanban sauce lifted with spoon. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G11 — tartar: eggs, onion, mayo (s35, s36, s37, s38; 6 s)

Original per-cut text (unchanged):
- `s35`: Close shot of two peeled hard-boiled eggs placed in glass bowl.
- `s36`: Macro fork mashing boiled eggs into small chunks.
- `s37`: Same man finely dicing onion on wooden cutting board.
- `s38`: Mayonnaise squeezed into mashed egg and chopped onion.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 4 shots in 6.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.50s, storyboard s35): Close shot of two peeled hard-boiled eggs placed in glass bowl. Shot 2 (1.50-3.00s, storyboard s36): Macro fork mashing boiled eggs into small chunks. Shot 3 (3.00-4.50s, storyboard s37): Same man finely dicing onion on wooden cutting board. Shot 4 (4.50-6.00s, storyboard s38): Mayonnaise squeezed into mashed egg and chopped onion. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G12 — tartar: mixing and tasting (s39, s40, s41, s42; 6 s)

Original per-cut text (unchanged):
- `s39`: Hands mixing chunky creamy tartar sauce with spoon.
- `s40`: Macro of creamy pale egg tartar sauce with chopped onion.
- `s41`: Same man tasting a cooled drop of sauce safely from a spoon.
- `s42`: Two glass bowls of glossy brown nanban sauce and creamy egg tartar side by side.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 4 shots in 6.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.50s, storyboard s39): Hands mixing chunky creamy tartar sauce with spoon. Shot 2 (1.50-3.00s, storyboard s40): Macro of creamy pale egg tartar sauce with chopped onion. Shot 3 (3.00-4.50s, storyboard s41): Same man tasting a cooled drop of sauce safely from a spoon. Shot 4 (4.50-6.00s, storyboard s42): Two glass bowls of glossy brown nanban sauce and creamy egg tartar side by side. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G13 — coating in sauce (s43, s44, s45, s46; 6 s)

Original per-cut text (unchanged):
- `s43`: Macro crisp golden fried chicken resting on rack.
- `s44`: Tongs dipping cooked golden chicken into prepared nanban sauce in glass bowl.
- `s45`: Close chopsticks gently tossing cooked chicken in sauce.
- `s46`: Extreme macro of glossy nanban-coated chicken.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 4 shots in 6.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.50s, storyboard s43): Macro crisp golden fried chicken resting on rack. Shot 2 (1.50-3.00s, storyboard s44): Tongs dipping cooked golden chicken into prepared nanban sauce in glass bowl. Shot 3 (3.00-4.50s, storyboard s45): Close chopsticks gently tossing cooked chicken in sauce. Shot 4 (4.50-6.00s, storyboard s46): Extreme macro of glossy nanban-coated chicken. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G14 — plating: rice, cabbage, chicken (s47, s48, s49, s50; 6 s)

Original per-cut text (unchanged):
- `s47`: Same man scooping white rice into striped ceramic bowl.
- `s48`: Close shot of shredded cabbage placed on serving plate.
- `s49`: Tongs arranging glazed chicken next to shredded cabbage on plate.
- `s50`: Macro adding more glazed pieces into inviting mound.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 4 shots in 6.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.50s, storyboard s47): Same man scooping white rice into striped ceramic bowl. Shot 2 (1.50-3.00s, storyboard s48): Close shot of shredded cabbage placed on serving plate. Shot 3 (3.00-4.50s, storyboard s49): Tongs arranging glazed chicken next to shredded cabbage on plate. Shot 4 (4.50-6.00s, storyboard s50): Macro adding more glazed pieces into inviting mound. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G15 — plating: sauce, tartar, parsley (s51, s52, s53, s54; 6 s)

Original per-cut text (unchanged):
- `s51`: Close shot of shiny nanban sauce drizzled over plated chicken.
- `s52`: Chunky cream-colored homemade tartar sauce spooned atop chicken.
- `s53`: Fresh chopped parsley falling over tartar.
- `s54`: Top-down finished chicken nanban platter, tartar, cabbage garnish.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 4 shots in 6.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.50s, storyboard s51): Close shot of shiny nanban sauce drizzled over plated chicken. Shot 2 (1.50-3.00s, storyboard s52): Chunky cream-colored homemade tartar sauce spooned atop chicken. Shot 3 (3.00-4.50s, storyboard s53): Fresh chopped parsley falling over tartar. Shot 4 (4.50-6.00s, storyboard s54): Top-down finished chicken nanban platter, tartar, cabbage garnish. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G16 — to the table (s55, s56; 4 s)

Original per-cut text (unchanged):
- `s55`: Same man carrying finished plate to wooden dining table.
- `s56`: Same man sitting at table, hands together saying itadakimasu, chicken nanban and rice.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 2 shots in 4.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-2.00s, storyboard s55): Same man carrying finished plate to wooden dining table. Shot 2 (2.00-4.00s, storyboard s56): Same man sitting at table, hands together saying itadakimasu, chicken nanban and rice. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Keep the room identical to the separate kitchen environment reference. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G17 — eating: first bite (s57, s58, s59, s60; 6 s)

Original per-cut text (unchanged):
- `s57`: Chopsticks lifting a piece of chicken nanban topped with tartar.
- `s58`: Extreme macro chunky tartar and golden fried crust.
- `s59`: Same man taking a single bite with chopsticks.
- `s60`: Macro cross section of fully cooked white chicken and crisp golden coating.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 4 shots in 6.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.50s, storyboard s57): Chopsticks lifting a piece of chicken nanban topped with tartar. Shot 2 (1.50-3.00s, storyboard s58): Extreme macro chunky tartar and golden fried crust. Shot 3 (3.00-4.50s, storyboard s59): Same man taking a single bite with chopsticks. Shot 4 (4.50-6.00s, storyboard s60): Macro cross section of fully cooked white chicken and crisp golden coating. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G18 — eating: reactions (s61, s62, s63, s64; 6 s)

Original per-cut text (unchanged):
- `s61`: Close portrait, same man eyes closed enjoying flavorful bite.
- `s62`: Same man eating white rice from ceramic bowl.
- `s63`: Extreme macro of glossy chicken nanban sauce and tartar.
- `s64`: Spoon lifting chunky fresh egg tartar from bowl.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 4 shots in 6.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.50s, storyboard s61): Close portrait, same man eyes closed enjoying flavorful bite. Shot 2 (1.50-3.00s, storyboard s62): Same man eating white rice from ceramic bowl. Shot 3 (3.00-4.50s, storyboard s63): Extreme macro of glossy chicken nanban sauce and tartar. Shot 4 (4.50-6.00s, storyboard s64): Spoon lifting chunky fresh egg tartar from bowl. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G19 — eating: water and table (s65, s66, s67; 5 s)

Original per-cut text (unchanged):
- `s65`: Same man drinking water from clear glass.
- `s66`: Wide kitchen dining shot with same man enjoying his home-cooked dinner.
- `s67`: Close partly eaten chicken nanban plate, remaining cabbage and sauce.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 3 shots in 5.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.67s, storyboard s65): Same man drinking water from clear glass. Shot 2 (1.67-3.34s, storyboard s66): Wide kitchen dining shot with same man enjoying his home-cooked dinner. Shot 3 (3.34-5.00s, storyboard s67): Close partly eaten chicken nanban plate, remaining cabbage and sauce. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Keep the room identical to the separate kitchen environment reference. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```

### G20 — finish (s68, s69, s70; 5 s)

Original per-cut text (unchanged):
- `s68`: Chopsticks picking up the last bite of chicken.
- `s69`: Same man leaning back with a satisfied relaxed breath.
- `s70`: Cinematic hero shot of finished chicken nanban with tartar, shredded cabbage and tomatoes.

Draft generation prompt:

```
MULTI-SHOT SEQUENCE: exactly 3 shots in 5.0 seconds, hard cut between shots, no other shots. Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. Each shot is one continuous take showing only its own action. Shot 1 (0.00-1.67s, storyboard s68): Chopsticks picking up the last bite of chicken. Shot 2 (1.67-3.34s, storyboard s69): Same man leaning back with a satisfied relaxed breath. Shot 3 (3.34-5.00s, storyboard s70): Cinematic hero shot of finished chicken nanban with tartar, shredded cabbage and tomatoes. Warm hand-drawn semi-realistic anime food illustration, ink outlines, subtle watercolor/marker shading, cinematic framing. A single consistent young Japanese man in his twenties with tousled black hair wearing a plain white T-shirt, the same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils. Vertical 9:16. No captions, no watermarks. Maintain continuity with the attached storyboard reference panel. Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands. Keep the room identical to the separate kitchen environment reference. Natural cooking sounds only, no music, no speech. Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, extra people, overlay text, logos or watermarks.
```
