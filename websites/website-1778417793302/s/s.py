import sys
import os
import json
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6 import uic


class ManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), "gui", "main.ui")
        uic.loadUi(ui_path, self)

        self.btnExport.clicked.connect(self.export_data)

        self.load_data()

    def load_data(self):
        self.AnimeList.clear()

        try:
            base_dir = os.path.dirname(__file__)
            file_path = os.path.join(base_dir, "anime.json")
            with open(file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)

            for item in self.data:
                text = f"Name: {item['name']} - Episodes: {item['episodes']}"
                self.AnimeList.addItem(text)

        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không đọc được file JSON\n{e}")

    def export_data(self):
        output_data = []

        for i in range(self.AnimeList.count()):
            text = self.AnimeList.item(i).text()

            try:
                parts = text.replace("Name: ", "").split(" - Episodes: ")
                name = parts[0]
                episodes = int(parts[1])

                output_data.append({
                    "name": name,
                    "episodes": episodes
                })
            except:
                QMessageBox.warning(self, "Lỗi", "Dữ liệu không hợp lệ!")
                return

        try:
            with open("output.json", "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=4, ensure_ascii=False)

            QMessageBox.information(self, "Thành công", "Đã export dữ liệu!")

        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Ghi file thất bại\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ManagerApp()
    window.show()
    sys.exit(app.exec())