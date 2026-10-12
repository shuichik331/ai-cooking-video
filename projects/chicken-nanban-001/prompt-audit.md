# Prompt audit — chicken-nanban-001

Read-only check of `prompts.json` against the s01 success pattern (`docs/seedance-scene-template.md`). Claude Code has not edited any prompt; ChatGPT does the final edit.

Scenes audited: 69 (excluded: s01)

| finding | scenes | severity |
|---|---|---|
| `recipe-sentence` | 69 | high |
| `no-single-shot` | 69 | high |
| `open-discrepancy` | 4 | high |
| `no-exclusions` | 69 | medium |
| `no-duration` | 69 | medium |
| `generic-camera` | 69 | medium |
| `generic-motion` | 69 | medium |
| `no-reference-roles` | 69 | medium |
| `face-visible` | 16 | low |
| `wide-panel` | 10 | low |
| `recorded-discrepancy` | 1 | low |

## Per scene

| id | shot | high | medium/low |
|---|---|---|---|
| s02 | 冷蔵庫を開ける | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s03 | 鶏もも肉を取り出す | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible |
| s04 | 材料を並べる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s05 | まな板に鶏肉を置く | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s06 | 鶏肉を一口大に切る | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s07 | 鶏肉の筋を切る | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s08 | 塩こしょうを振る | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible |
| s09 | ボウルに卵を割る | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s10 | 卵を溶く | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s11 | 小麦粉を用意 | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s12 | 鶏肉に粉をまぶす | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s13 | 卵液にくぐらせる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, wide-panel |
| s14 | 衣をまとった鶏肉の寄り | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, wide-panel |
| s15 | フライパンに油を注ぐ | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible |
| s16 | 油温を確かめる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s17 | 鶏肉を油に入れる | recipe-sentence; no-single-shot; open-discrepancy: Image: bare fingers lower a flour-coated piece into the oil. prompts.json: 'battered chicken being carefully lowered into hot oil with tongs'. Utensil (and batter look) differ. | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s18 | 泡立つ油の寄り | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s19 | 鶏肉を追加する | recipe-sentence; no-single-shot; open-discrepancy: Image: bare fingers add pieces to the hot oil. prompts.json: 'Close hands adding the next chicken pieces with tongs'. Utensil differs (also a hand-safety concern). | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s20 | 真上の揚げる全景 | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s21 | 膨らむ衣のアップ | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s22 | 男性がコンロを見守る | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible |
| s23 | 菜箸で返す | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s24 | 黄金色に変わる衣 | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s25 | 鶏肉を網に上げる | recipe-sentence; no-single-shot; open-discrepancy: Image: chopsticks lift a piece above the frying pan, no rack in frame. prompts.json: 'Tongs lifting fully cooked golden chicken onto wire rack'. Utensil and destination differ. | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s26 | 油を切る | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, recorded-discrepancy |
| s27 | 残りの鶏肉を揚げる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, wide-panel |
| s28 | 揚がった鶏肉を並べる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, wide-panel |
| s29 | 小鍋に酢を注ぐ | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible |
| s30 | 醤油を注ぐ | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s31 | 砂糖を加える | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s32 | 鍋を加熱する | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s33 | 南蛮だれが煮立つ | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s34 | タレの艶のアップ | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s35 | ゆで卵を置く | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s36 | ゆで卵をつぶす | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s37 | 玉ねぎをみじん切り | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible |
| s38 | マヨネーズを加える | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s39 | タルタルを混ぜる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s40 | タルタルソース完成 | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s41 | 南蛮だれを味見する | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible, wide-panel |
| s42 | 南蛮だれとタルタルを並べる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, wide-panel |
| s43 | 揚げた鶏肉の寄り | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s44 | 鶏肉を南蛮だれに入れる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s45 | 南蛮だれを絡める | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s46 | 艶やかな鶏肉アップ | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s47 | ご飯を茶碗によそう | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible |
| s48 | 千切りキャベツを皿に盛る | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s49 | 鶏肉を盛り付ける | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s50 | 鶏肉を高く盛る | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s51 | 南蛮だれを回しかける | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s52 | タルタルソースをのせる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s53 | パセリを散らす | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s54 | 完成皿の真上ショット | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s55 | 料理をテーブルに運ぶ | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible, wide-panel |
| s56 | 男性が座っていただきます | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible, wide-panel |
| s57 | 箸で鶏肉を持ち上げる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s58 | タルタルの寄り | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s59 | 男性が一口かじる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible |
| s60 | 鶏肉の断面アップ | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s61 | 男性の満足した表情 | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible |
| s62 | 男性がご飯を食べる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible |
| s63 | 鶏肉の艶アップ | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s64 | タルタルをすくう | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s65 | 男性が水を飲む | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible |
| s66 | 食卓の引きショット | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible |
| s67 | 食べ進んだ皿 | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s68 | 最後の一個を持ち上げる | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles |
| s69 | 男性が満足して息をつく | recipe-sentence; no-single-shot | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, face-visible, wide-panel |
| s70 | 完成皿のヒーローショット | recipe-sentence; no-single-shot; open-discrepancy: Image and prompt both show tomatoes, but no tomato appears in the plating sequence s48–s54 or in s67. Continuity question for the creative lead. | no-exclusions, no-duration, generic-camera, generic-motion, no-reference-roles, wide-panel |
