"""
Windows Dual Audio Bridge (WASAPI Loopback)
Outputs real-time audio from default playback device to a secondary device.
Supports on-the-fly dynamic resampling between different sample rates (e.g. 44.1kHz <-> 48kHz).
"""

import sys
import time
import argparse
import numpy as np
import pyaudiowpatch as pyaudio

def get_devices(p):
    try:
        wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
    except OSError:
        print("[HATA] Windows WASAPI ses sistemi bulunamadı!")
        return None, None, []

    default_output_idx = wasapi_info["defaultOutputDevice"]
    default_dev = p.get_device_info_by_index(default_output_idx)

    # Find loopback device for the default playback endpoint
    loopback_dev = None
    for dev in p.get_loopback_device_info_generator():
        if dev["name"].startswith(default_dev["name"]):
            loopback_dev = dev
            break

    # Find all available secondary output devices
    targets = []
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev["hostApi"] == wasapi_info["index"] and dev["maxOutputChannels"] > 0 and not dev["isLoopbackDevice"]:
            if i != default_output_idx:
                targets.append((i, dev))

    return default_dev, loopback_dev, targets

def start_mirroring(target_index=None):
    p = pyaudio.PyAudio()
    default_dev, loopback_dev, targets = get_devices(p)

    if not default_dev or not loopback_dev:
        print("[HATA] Birincil ses çıkışı veya dinleyici aygıtı bulunamadı.")
        p.terminate()
        return

    print("=" * 60)
    print("   WINDOWS 11 ÇİFT KULAKLIK SES AKTARICI (DUAL AUDIO)")
    print("=" * 60)
    print(f"[*] 1. Kulaklık (Ana Çıkış): {default_dev['name']}")

    if not targets:
        print("[!] Bağlı başka bir ses çıkışı / kulaklık bulunamadı!")
        print("    Lütfen 2. kulaklığınızı (3.5mm jak, USB veya Bluetooth) bağlayın.")
        p.terminate()
        return

    selected_target = None
    if target_index is not None:
        for idx, dev in targets:
            if idx == target_index:
                selected_target = dev
                break

    if not selected_target:
        if len(targets) == 1:
            selected_target = targets[0][1]
        else:
            print("\n2. Kulaklık / Çıkış Aygıtını Seçin:")
            for i, (idx, dev) in enumerate(targets):
                print(f"  [{idx}] {dev['name']}")
            choice = input("\nAygıt numarasını girin (Varsayılan için Enter): ").strip()
            if choice and choice.isdigit():
                c_idx = int(choice)
                for idx, dev in targets:
                    if idx == c_idx:
                        selected_target = dev
                        break
            if not selected_target:
                selected_target = targets[0][1]

    print(f"[*] 2. Kulaklık (İkinci Çıkış): {selected_target['name']}")
    print("-" * 60)

    in_rate = int(loopback_dev["defaultSampleRate"])
    out_rate = int(selected_target["defaultSampleRate"])
    in_channels = loopback_dev["maxInputChannels"]
    out_channels = min(2, selected_target["maxOutputChannels"])

    out_stream = p.open(
        format=pyaudio.paInt16,
        channels=out_channels,
        rate=out_rate,
        output=True,
        output_device_index=selected_target["index"],
        frames_per_buffer=1024
    )

    def audio_callback(in_data, frame_count, time_info, status):
        try:
            if in_rate != out_rate:
                arr = np.frombuffer(in_data, dtype=np.int16).reshape(-1, in_channels)
                n_in = len(arr)
                n_out = int(round(n_in * out_rate / in_rate))
                t_in = np.arange(n_in)
                t_out = np.linspace(0, n_in - 1, n_out)
                res = np.empty((n_out, in_channels), dtype=np.int16)
                for c in range(in_channels):
                    res[:, c] = np.interp(t_out, t_in, arr[:, c])
                out_stream.write(res.tobytes())
            else:
                out_stream.write(in_data)
        except Exception:
            pass
        return (None, pyaudio.paContinue)

    in_stream = p.open(
        format=pyaudio.paInt16,
        channels=in_channels,
        rate=in_rate,
        input=True,
        input_device_index=loopback_dev["index"],
        frames_per_buffer=1024,
        stream_callback=audio_callback
    )

    in_stream.start_stream()
    print("\n[BAŞARILI] Ses her iki kulaklığa da anında aktarılıyor!")
    print("Durdurmak için pencereyi kapatabilir veya Ctrl+C yapabilirsiniz.\n")

    try:
        while in_stream.is_active():
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nAktarım durduruluyor...")
    finally:
        in_stream.stop_stream()
        in_stream.close()
        out_stream.stop_stream()
        out_stream.close()
        p.terminate()
        print("Tamamlandı.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Windows Dual Audio Bridge")
    parser.add_argument("--target", type=int, default=None, help="Hedef aygıt index numarası")
    args = parser.parse_args()
    start_mirroring(args.target)
