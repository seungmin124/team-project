import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

# =========================
# 1. 랜덤 비트 생성 , 100개
# =========================
N = 100

bits = np.random.randint(0, 2, N)

print("원본 비트:")
print(bits)

# =========================
# 2. 채널 코딩 (3회 반복)
# =========================
coded_bits = np.repeat(bits, 3)

print("채널코딩 후:")
print(coded_bits)

print("원본 비트 개수:", len(bits))
print("채널코딩 후 비트 개수:", len(coded_bits))

# =========================
# 3. 2비트씩 묶기
# =========================
symbols_bits = coded_bits.reshape(-1, 2)

print("2비트씩 묶기:")
print(symbols_bits)

# =========================
# 4. QPSK 매핑
# =========================
qpsk_symbols = []

for pair in symbols_bits:

    if (pair == [0, 0]).all():
        qpsk_symbols.append(1 + 1j)

    elif (pair == [0, 1]).all():
        qpsk_symbols.append(1 - 1j)

    elif (pair == [1, 0]).all():
        qpsk_symbols.append(-1 + 1j)

    else:
        qpsk_symbols.append(-1 - 1j)

print("QPSK 심볼 개수:", len(qpsk_symbols))

# =========================
# 5. 성상도
# =========================
plt.figure()

plt.scatter(
    [s.real for s in qpsk_symbols],
    [s.imag for s in qpsk_symbols]
)

plt.grid()
plt.xlabel("In-Phase (I)")
plt.ylabel("Quadrature (Q)")
plt.title("QPSK Constellation")

plt.show()

# =========================
# 6. 업샘플링 , 실제 통신은 연속 신호라서 시간 확장 필요
# =========================
sps = 8

upsampled = np.zeros(len(qpsk_symbols) * sps, dtype=complex)

upsampled[::sps] = qpsk_symbols

print("업샘플링 후 길이:", len(upsampled))

# =========================
# 7. 직사각형 펄스 쉐이핑
# =========================
pulse = np.ones(sps)

tx_signal = convolve(upsampled, pulse)

print("펄스 쉐이핑 후 길이:", len(tx_signal))

# =========================
# 8. I/Q 파형 확인
# =========================
plt.figure(figsize=(10, 5))

plt.plot(tx_signal.real,
         label="I (In-Phase)",
         linewidth=3)

plt.plot(tx_signal.imag,
         label="Q (Quadrature)",
         linewidth=1)

plt.title("Pulse Shaping Signal")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

plt.show()

# =========================
# 9. I/Q 값 출력
# =========================
print("I 성분:")
print([s.real for s in qpsk_symbols])

print("Q 성분:")
print([s.imag for s in qpsk_symbols])