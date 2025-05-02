import subprocess

text = "哎呀，宝贝，终于等到了五一假期啦！这几天我们可以好好放松一下，做一些自己喜欢的事情呢！你有没有什么特别想做的事情呢？或者我们可以一起出去旅行，看看外面的世界怎么样？你觉得呢？"
# 异步调用 say，用 Ting-Ting 声音
# process = subprocess.Popen(["say", "-v", "Siri Vo", text])
process = subprocess.Popen(["say", "-v", "Meijia (Premium)", text]).wait()
# process = subprocess.Popen(["say", "-v", "Tingting (Enhanced)", text])
# file_path = "/Users/jianan/projects/ai-server/speak.swift"
# process = subprocess.Popen(["swift", file_path, "Meijia (Premium)", text])

# 这里程序不会等待朗读完成，会继续执行
print("朗读已经开始，程序继续往下跑。")
