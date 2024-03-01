import sys
from PySide6.QtWidgets import QApplication, QLabel, QComboBox, QVBoxLayout, QWidget



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建主窗口
    window = QWidget()
    #设置窗口标题
    window.setWindowTitle("简单的QComboBox例子")
    window.setGeometry(100,100,200,200)
    # 创建布局
    layout = QVBoxLayout()

    #创建标签
    label = QLabel("选择一个项：")

    #创建下拉框
    combo_box = QComboBox()

    #向下拉框添加选项
    combo_box.addItem("选项1")
    combo_box.addItem("选项2")
    combo_box.addItem("选项3")

    #将标签和下拉框添加到布局
    layout.addWidget(label)
    layout.addWidget(combo_box)

    #将布局设置为主窗口的布局
    window.setLayout(layout)

    #定义下拉框选择变化时的槽函数
    def on_combobox_changed(index):
        selected_text = combo_box.currentText()
        label.setText(f"选择的项是：{selected_text}")

    #将下拉框的选择改变事件连接到槽函数
    combo_box.currentIndexChanged.connect(on_combobox_changed)

    #显示主窗口
    window.show()

    sys.exit(app.exec())
