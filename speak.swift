import AVFoundation
import Foundation

// 取出命令行第一个参数（index 1）
guard CommandLine.arguments.count > 1 else {
    print("❗️请在命令后输入要朗读的内容，例如：swift speak.swift \"你好，世界！\"")
    exit(1)
}

let input = CommandLine.arguments[2]

// 创建语音合成器
let synthesizer = AVSpeechSynthesizer()

// 创建朗读对象
let utterance = AVSpeechUtterance(string: input)


let voices = AVSpeechSynthesisVoice.speechVoices()
for voice in voices {
    print("Voice identifier: \(voice.identifier), language: \(voice.language), name: \(voice.name)")
}

// 设置语音
if let voice = AVSpeechSynthesisVoice(identifier: "com.apple.voice.enhanced.zh-CN.Tingting") {
    utterance.voice = voice
}

// utterance.rate = 0.5
// utterance.pitchMultiplier = 1.0

// 开始朗读
synthesizer.speak(utterance)

// 防止程序立即退出
RunLoop.main.run()
