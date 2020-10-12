# kanjiRemember
A Tkinter App help you remember Kanjis :D


## Xem lại cái kiến trúc xí
Ui vãi loz vì tui tự nhiên kiến trúc phần mềm một cách khá là ngu loz. Cho nên cập nhật cái readme xí để
bản thân tự chủ được tình hình.

* Mình tạo một Kanji object:
    - Nó bao gồm: mặt kanji, hiragana, nghĩa Hán Việt, nghĩa, sound_url, sound_path.
    - Hai method: setSavedSoundFilePath, downloadSound.
* Nó sẽ có một script để đưa Kanji về file excel
* Mỗi lần người dùng load tới Kanji đó thì Kanji đó sẽ tự động tải về, lưu path, lưu file vào folder.

## Nói chung kiến trúc khá đơn giản như thế này :D
"Đối tượng sẽ phụ thuộc vào dữ liệu đã được clean, dữ liệu thô không thể phụ thuộc vào Đối tượng" -- Xin phán.
Sai lầm của mình là tạo ra một khung cho việc cào Kanji, đưa dữ liệu thô vào Kanji sau đó lưu vào excel, ngu vc.
Thật ra thì cái script cào nó chả liên quan đéo gì tới cái chương trình của mình cả.
Mà chỉ có file excel tương tác với chương trình.

Nhìn vào comment 1 rõ ràng theo ý của bạn là cái tên đó không được đặt. Nhưng sau 1 hồi tới comment 2 thì bạn là ủng hộ việc bạn đặt cái tên đó :D