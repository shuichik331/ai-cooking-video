# chicken-nanban-001: storyboard image ↔ JSON cross-check

Checked 2026-10-12 by Claude Code. All five pages were downloaded from Google Drive (sizes match Drive metadata; SHA-256 values are in `production-status.json → image_verification`) and every page was reviewed visually. No creative file was changed.

## Summary
- **70/70 panels present.** Panel numbers 01–70 run in order, page ranges match `pages.json` (14 panels per page), and every image timecode equals `storyboard.json` except s26.
- **Captions:** every image caption describes the same action as the JSON `shot`. Wording differs in places, for example s04, s24 and s56.
- **Recorded decision:** for s26 the image header reads '0:25 - 0:22'. Timing 0:25–0:26 from JSON is used, per user instruction. The original image is uncorrected, so a corrected page-02 image is requested.
- **Waiting on the creative lead (blocks full production, not the s01 test):**
  - s17 / s19 / s25: utensils differ between image and prompt.
  - s70: tomato continuity.
- **Consistency in the drawings:** the same protagonist throughout (tousled black hair, plain white T-shirt, dark trousers), the same kitchen (wooden counters, white fridge, plants, warm light) and one illustration style.

## Panel table

| id | page | image time | image caption | storyboard.json shot | check |
|---|---|---|---|---|---|
| s01 | 1 | 0:00 - 0:01 | 小さなキッチン全景 一人暮らしの朝 | 小さなキッチン全景 | Man seen from behind at the sink; caption says 'morning' |
| s02 | 1 | 0:01 - 0:02 | 冷蔵庫を開ける | 冷蔵庫を開ける | match |
| s03 | 1 | 0:02 - 0:03 | 鶏もも肉を取り出す | 鶏もも肉を取り出す | match |
| s04 | 1 | 0:03 - 0:04 | 卵・玉ねぎ・酢・醤油を並べる | 材料を並べる | Image also shows chicken tray and pepper mill (prompt: 'seasonings') |
| s05 | 1 | 0:04 - 0:05 | まな板に鶏肉を置く | まな板に鶏肉を置く | match |
| s06 | 1 | 0:05 - 0:06 | 包丁アップ / 一口大に切る | 鶏肉を一口大に切る | match |
| s07 | 1 | 0:06 - 0:07 | 手元アップ / 筋を切る | 鶏肉の筋を切る | match |
| s08 | 1 | 0:07 - 0:08 | 塩こしょうを振る | 塩こしょうを振る | match |
| s09 | 1 | 0:08 - 0:09 | ボウルに卵を割る | ボウルに卵を割る | match |
| s10 | 1 | 0:09 - 0:10 | 卵を溶く | 卵を溶く | match |
| s11 | 1 | 0:10 - 0:11 | 小麦粉の皿を用意 | 小麦粉を用意 | Flour in a white enamel tray with blue rim (prompt: 'shallow white dish') |
| s12 | 1 | 0:11 - 0:12 | 鶏肉に小麦粉をまぶす | 鶏肉に粉をまぶす | match |
| s13 | 1 | 0:12 - 0:13 | 卵液にくぐらせる | 卵液にくぐらせる | match |
| s14 | 1 | 0:13 - 0:14 | 衣をまとった鶏肉の寄り | 衣をまとった鶏肉の寄り | match |
| s15 | 2 | 0:14 - 0:15 | フライパンに油を注ぐ | フライパンに油を注ぐ | match |
| s16 | 2 | 0:15 - 0:16 | 菜箸で油温を確かめる | 油温を確かめる | match |
| s17 | 2 | 0:16 - 0:17 | 鶏肉を1つ油へ入れる | 鶏肉を油に入れる | **Conflict**: bare fingers in image vs 'with tongs' in prompt; piece looks flour-only |
| s18 | 2 | 0:17 - 0:18 | ジュワッと泡立つ油の寄り | 泡立つ油の寄り | match |
| s19 | 2 | 0:18 - 0:19 | 次々に鶏肉を入れる | 鶏肉を追加する | **Conflict**: bare fingers in image vs 'with tongs' in prompt |
| s20 | 2 | 0:19 - 0:20 | 真上ショット / 揚げる全景 | 真上の揚げる全景 | match |
| s21 | 2 | 0:20 - 0:21 | 衣がふくらむアップ | 膨らむ衣のアップ | match |
| s22 | 2 | 0:21 - 0:22 | コンロ前で見守る | 男性がコンロを見守る | match |
| s23 | 2 | 0:22 - 0:23 | 菜箸で返す | 菜箸で返す | match |
| s24 | 2 | 0:23 - 0:24 | きつね色になり始める | 黄金色に変わる衣 | match |
| s25 | 2 | 0:24 - 0:25 | 網に上げる | 鶏肉を網に上げる | **Conflict**: chopsticks over the pan in image vs 'tongs … onto wire rack' in prompt |
| s26 | 2 | 0:25 - **0:22** | 油を切るアップ | 油を切る | **Timecode**: image header '0:25 - 0:22'; JSON 25–26s is used (user decision) |
| s27 | 2 | 0:26 - 0:27 | 2回目のバッチを揚げる | 残りの鶏肉を揚げる | match |
| s28 | 2 | 0:27 - 0:28 | 揚がった鶏肉が並ぶ | 揚がった鶏肉を並べる | match |
| s29 | 3 | 0:28 - 0:29 | 小鍋に酢を入れる | 小鍋に酢を注ぐ | match |
| s30 | 3 | 0:29 - 0:30 | 醤油を注ぐ | 醤油を注ぐ | match |
| s31 | 3 | 0:30 - 0:31 | 砂糖を加える | 砂糖を加える | match |
| s32 | 3 | 0:31 - 0:32 | 火にかける | 鍋を加熱する | match |
| s33 | 3 | 0:32 - 0:33 | 泡立つ南蛮だれ | 南蛮だれが煮立つ | match |
| s34 | 3 | 0:33 - 0:34 | 照りのあるタレの寄り | タレの艶のアップ | match |
| s35 | 3 | 0:34 - 0:35 | ゆで卵を置く | ゆで卵を置く | match |
| s36 | 3 | 0:35 - 0:36 | ゆで卵をつぶす | ゆで卵をつぶす | match |
| s37 | 3 | 0:36 - 0:37 | 玉ねぎをみじん切り | 玉ねぎをみじん切り | match |
| s38 | 3 | 0:37 - 0:38 | マヨネーズを加える | マヨネーズを加える | match |
| s39 | 3 | 0:38 - 0:39 | ボウルで混ぜる | タルタルを混ぜる | match |
| s40 | 3 | 0:39 - 0:40 | タルタルソース完成 | タルタルソース完成 | Image shows black pepper on the tartar (not in prompt) |
| s41 | 3 | 0:40 - 0:41 | 南蛮だれを味見 | 南蛮だれを味見する | match |
| s42 | 3 | 0:41 - 0:42 | タレとタルタルを並べる | 南蛮だれとタルタルを並べる | match |
| s43 | 4 | 0:42 - 0:43 | 揚げた鶏肉をもう一度寄り | 揚げた鶏肉の寄り | match |
| s44 | 4 | 0:43 - 0:44 | 鶏肉を南蛮だれへ入れる | 鶏肉を南蛮だれに入れる | match |
| s45 | 4 | 0:44 - 0:45 | タレを絡める | 南蛮だれを絡める | match |
| s46 | 4 | 0:45 - 0:46 | ツヤツヤの表面アップ | 艶やかな鶏肉アップ | match |
| s47 | 4 | 0:46 - 0:47 | ご飯を茶碗によそう | ご飯を茶碗によそう | match |
| s48 | 4 | 0:47 - 0:48 | 千切りキャベツを皿へ | 千切りキャベツを皿に盛る | match |
| s49 | 4 | 0:48 - 0:49 | 鶏肉を盛り付ける | 鶏肉を盛り付ける | match |
| s50 | 4 | 0:49 - 0:50 | さらに盛って高さを出す | 鶏肉を高く盛る | match |
| s51 | 4 | 0:50 - 0:51 | 南蛮だれを回しかける | 南蛮だれを回しかける | match |
| s52 | 4 | 0:51 - 0:52 | タルタルをのせる | タルタルソースをのせる | match |
| s53 | 4 | 0:52 - 0:53 | パセリを散らす | パセリを散らす | match |
| s54 | 4 | 0:53 - 0:54 | 完成皿の真上ショット | 完成皿の真上ショット | match |
| s55 | 4 | 0:54 - 0:55 | テーブルへ運ぶ | 料理をテーブルに運ぶ | match |
| s56 | 4 | 0:55 - 0:56 | 椅子に座る | 男性が座っていただきます | Image also shows miso soup and a water glass (not in prompt) |
| s57 | 5 | 0:56 - 0:57 | 箸で1つ持ち上げる | 箸で鶏肉を持ち上げる | match |
| s58 | 5 | 0:57 - 0:58 | タルタルたっぷりの寄り | タルタルの寄り | match |
| s59 | 5 | 0:58 - 0:59 | ひと口かじる | 男性が一口かじる | match |
| s60 | 5 | 0:59 - 1:00 | サクッと断面アップ | 鶏肉の断面アップ | match |
| s61 | 5 | 1:00 - 1:01 | うまい表情 | 男性の満足した表情 | match |
| s62 | 5 | 1:01 - 1:02 | ご飯を食べる | 男性がご飯を食べる | match |
| s63 | 5 | 1:02 - 1:03 | チキン南蛮の艶寄り | 鶏肉の艶アップ | match |
| s64 | 5 | 1:03 - 1:04 | タルタルをすくう | タルタルをすくう | match |
| s65 | 5 | 1:04 - 1:05 | 水をひと口飲む | 男性が水を飲む | match |
| s66 | 5 | 1:05 - 1:06 | 食卓の引きショット | 食卓の引きショット | Prompt says 'dinner'; images are warm daylight (s01 caption: morning) |
| s67 | 5 | 1:06 - 1:07 | 皿が減っていく | 食べ進んだ皿 | match |
| s68 | 5 | 1:07 - 1:08 | 最後の1個を持ち上げる | 最後の一個を持ち上げる | match |
| s69 | 5 | 1:08 - 1:09 | 満足して息をつく | 男性が満足して息をつく | match |
| s70 | 5 | 1:09 - 1:10 | 完成皿のヒーローショット | 完成皿のヒーローショット | **Continuity**: tomatoes in image and prompt but absent from plating s48–s54 and s67 |
