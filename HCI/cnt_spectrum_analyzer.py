#!/usr/bin/env python3
"""
CNT Compositional Spectrum Analyzer
====================================

Program 3 of the CNT standard pipeline.

A Smaart-class spectral analysis instrument for compositional data,
operating in CLR (Higgins Coordinate) space via direct tensor math.

Input:  JSON output from cnt_tensor_engine.py
Output: Multi-page PDF with spectral plates:
  Page 1:  System Overview — CLR trajectory + Hs profile + angular velocity
  Page 2:  Magnitude Spectrum — FFT power of each CLR carrier channel
  Page 3:  Phase Response — FFT phase of each carrier channel
  Page 4:  Cross-Spectral Transfer Function — H(f) between carrier pairs
  Page 5:  Coherence Map — frequency-dependent correlation between pairs
  Page 6:  Group Delay — d(phase)/d(frequency) per carrier
  Page 7:  Impulse Response — autocorrelation of CLR channels
  Page 8:  Waterfall (Spectrogram) — STFT time-frequency decomposition
  Page 9:  Cepstrum — periodicity detector in spectral domain
  Page 10: Vector Field — CLR velocity magnitude + direction over time
  Page 11: Metric Tensor Trace + Condition Number evolution
  Page 12: Navigation Summary — complete measurement dashboard
  Page 13: Recursive Depth Sounding — tower trajectories + involution proof (requires --depth)
  Page 14: Convergence Characterization — residual decay + attractor portrait (requires --depth)

Design philosophy:
  - Vectorized FFT computation (no iterative face method)
  - Monochrome palette (instrument-grade, not decorative)
  - Fixed scales where applicable (full-range display)
  - All units in HLR (Higgins Log-Ratio Level)
  - Suitable for T=20 to T=1,000,000+

Smaart v9 mapping:
  Smaart spectrum      → CLR carrier FFT magnitude
  Smaart phase          → CLR carrier FFT phase
  Smaart transfer func  → Cross-spectral H(f) = Sxy/Sxx
  Smaart coherence      → |Sxy|^2 / (Sxx * Syy)
  Smaart impulse resp   → CLR autocorrelation
  Smaart spectrogram    → CLR Short-Time FFT

Mathematical lineage:
  Cooley-Tukey (1965)  — FFT algorithm
  Welch (1967)         — Power spectral density estimation
  Wiener-Khinchin      — Autocorrelation ↔ power spectrum
  Aitchison (1986)     — CLR transform
  Higgins (2026)       — CNT tensor, HCI instrument

Usage:
  python cnt_spectrum_analyzer.py engine_output.json [output.pdf]

The instrument reads. The expert decides. The loop stays open.
"""

import json
import math
import cmath
import sys
import os
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec
import numpy as np


# ══════════════════════════════════════════════════════════════════
# INSTRUMENT PALETTE (monochrome, instrument-grade)
# ══════════════════════════════════════════════════════════════════

BG_COLOR = '#0a0a0a'
FG_COLOR = '#e0e0e0'
GRID_COLOR = '#2a2a2a'
ACCENT_COLOR = '#4a9eff'
WARN_COLOR = '#ff6b6b'
# Carrier colors: grayscale gradient for monochrome feel
CARRIER_COLORS = [
    '#4a9eff', '#ff6b6b', '#6bff6b', '#ffff6b',
    '#ff6bff', '#6bffff', '#ffaa6b', '#aa6bff',
    '#6baaff', '#aaff6b', '#ff6baa', '#6bffaa',
]


def setup_axis(ax, title='', xlabel='', ylabel=''):
    """Configure axis for instrument-grade display."""
    ax.set_facecolor(BG_COLOR)
    ax.set_title(title, color=FG_COLOR, fontsize=10, fontweight='bold', pad=8)
    ax.set_xlabel(xlabel, color=FG_COLOR, fontsize=8)
    ax.set_ylabel(ylabel, color=FG_COLOR, fontsize=8)
    ax.tick_params(colors=FG_COLOR, labelsize=7)
    ax.spines['bottom'].set_color(GRID_COLOR)
    ax.spines['top'].set_color(GRID_COLOR)
    ax.spines['left'].set_color(GRID_COLOR)
    ax.spines['right'].set_color(GRID_COLOR)
    ax.grid(True, color=GRID_COLOR, alpha=0.5, linewidth=0.5)


def new_page(pdf, title, subtitle=''):
    """Create a new page with standard header."""
    fig = plt.figure(figsize=(11, 8.5), facecolor=BG_COLOR)
    fig.text(0.02, 0.97, 'CNT COMPOSITIONAL SPECTRUM ANALYZER',
             color=ACCENT_COLOR, fontsize=8, fontweight='bold',
             fontfamily='monospace', va='top')
    fig.text(0.02, 0.95, title,
             color=FG_COLOR, fontsize=12, fontweight='bold', va='top')
    if subtitle:
        fig.text(0.02, 0.925, subtitle,
                 color='#888888', fontsize=7, va='top')
    fig.text(0.98, 0.97, 'HCI / CNT v2.0',
             color='#555555', fontsize=7, ha='right', va='top',
             fontfamily='monospace')
    return fig


# ══════════════════════════════════════════════════════════════════
# FFT ENGINE (pure Python, vectorized via numpy)
# ══════════════════════════════════════════════════════════════════

def compute_fft(signal):
    """Compute FFT of a real signal. Returns (frequencies, magnitudes, phases).

    Frequencies are normalised to [0, 0.5] (Nyquist).
    """
    N = len(signal)
    arr = np.array(signal)
    # Remove DC (mean)
    arr = arr - np.mean(arr)
    # Apply Hanning window
    window = np.hanning(N)
    arr = arr * window
    # FFT
    spectrum = np.fft.rfft(arr)
    freqs = np.fft.rfftfreq(N)
    magnitudes = np.abs(spectrum) * 2.0 / N
    phases = np.angle(spectrum, deg=True)
    return freqs, magnitudes, phases


def compute_cross_spectrum(sig_x, sig_y):
    """Cross-spectral density via Welch averaging.

    Uses overlapping segments to produce meaningful coherence estimates.
    Single-segment FFT always gives gamma^2 = 1; Welch averaging with
    K segments produces coherence in [0, 1] with statistical significance
    threshold approximately 1 - alpha^(1/(K-1)).

    Returns (freqs, H_magnitude, H_phase, coherence).
    """
    N = len(sig_x)
    x = np.array(sig_x) - np.mean(sig_x)
    y = np.array(sig_y) - np.mean(sig_y)

    # Welch parameters: segment length and overlap
    # Target at least 4 segments for meaningful coherence
    seg_len = max(8, N // 4)
    overlap = seg_len // 2
    step = seg_len - overlap

    n_segments = max(1, (N - seg_len) // step + 1)
    window = np.hanning(seg_len)
    n_bins = seg_len // 2 + 1
    freqs = np.fft.rfftfreq(seg_len)

    # Accumulate averaged cross-spectral and auto-spectral densities
    Sxx_avg = np.zeros(n_bins)
    Syy_avg = np.zeros(n_bins)
    Sxy_avg = np.zeros(n_bins, dtype=complex)

    for k in range(n_segments):
        start = k * step
        end = start + seg_len
        if end > N:
            break
        X = np.fft.rfft(x[start:end] * window)
        Y = np.fft.rfft(y[start:end] * window)
        Sxx_avg += np.abs(X) ** 2
        Syy_avg += np.abs(Y) ** 2
        Sxy_avg += np.conj(X) * Y

    Sxx_avg /= n_segments
    Syy_avg /= n_segments
    Sxy_avg /= n_segments

    # Transfer function H(f) = Sxy / Sxx
    H_mag = np.abs(Sxy_avg) / np.maximum(Sxx_avg, 1e-30)
    H_phase = np.angle(Sxy_avg, deg=True)

    # Coherence gamma^2 = |<Sxy>|^2 / (<Sxx> * <Syy>)
    coherence = np.abs(Sxy_avg) ** 2 / np.maximum(Sxx_avg * Syy_avg, 1e-30)
    coherence = np.clip(coherence, 0, 1)

    return freqs, H_mag, H_phase, coherence


def compute_autocorrelation(signal):
    """Autocorrelation via Wiener-Khinchin theorem.

    R(tau) = IFFT(|FFT(x)|^2)
    """
    arr = np.array(signal) - np.mean(signal)
    N = len(arr)
    # Zero-pad for linear (not circular) autocorrelation
    padded = np.zeros(2 * N)
    padded[:N] = arr
    spectrum = np.fft.fft(padded)
    power = np.abs(spectrum) ** 2
    autocorr = np.real(np.fft.ifft(power))[:N]
    # Normalise
    if autocorr[0] > 0:
        autocorr = autocorr / autocorr[0]
    return autocorr


def compute_stft(signal, window_size=None, hop=None):
    """Short-Time Fourier Transform for waterfall/spectrogram.

    Returns (times, freqs, magnitude_matrix).
    """
    N = len(signal)
    if window_size is None:
        window_size = max(8, N // 8)
    if hop is None:
        hop = max(1, window_size // 2)

    arr = np.array(signal) - np.mean(signal)
    window = np.hanning(window_size)

    n_frames = max(1, (N - window_size) // hop + 1)
    n_bins = window_size // 2 + 1

    stft_matrix = np.zeros((n_bins, n_frames))
    times = []
    for i in range(n_frames):
        start = i * hop
        end = start + window_size
        if end > N:
            break
        segment = arr[start:end] * window
        spectrum = np.fft.rfft(segment)
        stft_matrix[:, i] = np.abs(spectrum)
        times.append(start + window_size // 2)

    freqs = np.fft.rfftfreq(window_size)
    return np.array(times), freqs, stft_matrix[:, :len(times)]


def compute_cepstrum(signal):
    """Real cepstrum: IFFT(log|FFT(x)|).

    Detects periodicity in the spectrum itself.
    """
    arr = np.array(signal) - np.mean(signal)
    N = len(arr)
    spectrum = np.fft.fft(arr)
    log_spectrum = np.log(np.maximum(np.abs(spectrum), 1e-30))
    cepstrum = np.real(np.fft.ifft(log_spectrum))
    return cepstrum[:N // 2]


def compute_group_delay(phases_deg, freqs):
    """Group delay: -d(phase)/d(freq).

    Negative derivative of unwrapped phase with respect to frequency.
    """
    if len(freqs) < 3:
        return np.zeros_like(freqs)
    phase_rad = np.unwrap(np.deg2rad(phases_deg))
    df = np.diff(freqs)
    dp = np.diff(phase_rad)
    # Guard against zero df
    df = np.where(df == 0, 1e-15, df)
    gd = -dp / df
    # Pad to same length
    gd = np.concatenate([gd, [gd[-1]]])
    return gd


# ══════════════════════════════════════════════════════════════════
# PAGE GENERATORS
# ══════════════════════════════════════════════════════════════════

def page1_overview(pdf, data):
    """Page 1: System Overview — CLR trajectories, Hs, angular velocity."""
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    labels = data["metadata"]["labels"]
    ts_data = data["timesteps"]

    fig = new_page(pdf, 'SYSTEM OVERVIEW',
                   f'D={D} carriers, T={T} steps, {labels[0]} → {labels[-1]}')

    gs = gridspec.GridSpec(3, 1, top=0.88, bottom=0.06, left=0.08,
                           right=0.92, hspace=0.35)

    # CLR trajectories
    ax1 = fig.add_subplot(gs[0])
    setup_axis(ax1, 'CLR Carrier Channels', ylabel='CLR [HLR]')
    t_axis = np.arange(T)
    for j in range(D):
        vals = [ts_data[t]["clr"][j] for t in range(T)]
        c = CARRIER_COLORS[j % len(CARRIER_COLORS)]
        ax1.plot(t_axis, vals, color=c, linewidth=1.0, alpha=0.9,
                 label=carriers[j])
    ax1.legend(fontsize=6, ncol=min(D, 4), loc='upper right',
               framealpha=0.3, facecolor=BG_COLOR, edgecolor=GRID_COLOR,
               labelcolor=FG_COLOR)

    # Hs profile
    ax2 = fig.add_subplot(gs[1])
    setup_axis(ax2, 'Higgins Scale', ylabel='Hs')
    hs_vals = [ts_data[t]["higgins_scale"] for t in range(T)]
    ax2.fill_between(t_axis, hs_vals, alpha=0.3, color=ACCENT_COLOR)
    ax2.plot(t_axis, hs_vals, color=ACCENT_COLOR, linewidth=1.5)
    ax2.set_ylim(0, 1)
    # Ring boundaries
    for rb in [0.05, 0.15, 0.30, 0.50, 0.75, 0.95]:
        ax2.axhline(y=rb, color=GRID_COLOR, linewidth=0.3, linestyle='--')

    # Angular velocity
    ax3 = fig.add_subplot(gs[2])
    setup_axis(ax3, 'Angular Velocity (omega)', xlabel='Time Index',
               ylabel='deg/step')
    omega_vals = [ts_data[t]["angular_velocity_deg"] for t in range(1, T)]
    ax3.bar(t_axis[1:], omega_vals, color=WARN_COLOR, alpha=0.7, width=0.8)

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page2_magnitude_spectrum(pdf, data):
    """Page 2: FFT Magnitude Spectrum of each CLR carrier channel."""
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    ts_data = data["timesteps"]

    fig = new_page(pdf, 'MAGNITUDE SPECTRUM',
                   f'FFT power spectral density per carrier (Hanning window, N={T})')

    n_rows = min(D, 4)
    n_cols = math.ceil(D / n_rows)
    gs = gridspec.GridSpec(n_rows, n_cols, top=0.88, bottom=0.06,
                           left=0.08, right=0.95, hspace=0.45, wspace=0.3)

    for j in range(D):
        row = j % n_rows
        col = j // n_rows
        ax = fig.add_subplot(gs[row, col])
        signal = [ts_data[t]["clr"][j] for t in range(T)]
        freqs, mags, _ = compute_fft(signal)

        # Plot in dB
        mags_db = 20 * np.log10(np.maximum(mags, 1e-15))
        c = CARRIER_COLORS[j % len(CARRIER_COLORS)]
        ax.plot(freqs[1:], mags_db[1:], color=c, linewidth=1.0)
        ax.fill_between(freqs[1:], mags_db[1:], min(mags_db[1:]) - 3,
                         alpha=0.2, color=c)
        setup_axis(ax, carriers[j], xlabel='Norm. Freq', ylabel='dB')

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page3_phase_response(pdf, data):
    """Page 3: FFT Phase Response of each CLR carrier channel."""
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    ts_data = data["timesteps"]

    fig = new_page(pdf, 'PHASE RESPONSE',
                   f'FFT phase angle per carrier (unwrapped)')

    n_rows = min(D, 4)
    n_cols = math.ceil(D / n_rows)
    gs = gridspec.GridSpec(n_rows, n_cols, top=0.88, bottom=0.06,
                           left=0.08, right=0.95, hspace=0.45, wspace=0.3)

    for j in range(D):
        row = j % n_rows
        col = j // n_rows
        ax = fig.add_subplot(gs[row, col])
        signal = [ts_data[t]["clr"][j] for t in range(T)]
        freqs, _, phases = compute_fft(signal)
        c = CARRIER_COLORS[j % len(CARRIER_COLORS)]
        ax.plot(freqs[1:], phases[1:], color=c, linewidth=0.8)
        setup_axis(ax, carriers[j], xlabel='Norm. Freq', ylabel='Phase [deg]')

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page4_transfer_function(pdf, data):
    """Page 4: Cross-spectral transfer function between top carrier pairs."""
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    ts_data = data["timesteps"]

    fig = new_page(pdf, 'TRANSFER FUNCTION H(f)',
                   'Cross-spectral magnitude: H(f) = Sxy(f) / Sxx(f)')

    # Select top pairs (up to 6)
    pairs = []
    for i in range(D):
        for j in range(i + 1, D):
            pairs.append((i, j))
    pairs = pairs[:6]

    n_rows = min(len(pairs), 3)
    n_cols = math.ceil(len(pairs) / n_rows)
    gs = gridspec.GridSpec(n_rows, n_cols, top=0.88, bottom=0.06,
                           left=0.08, right=0.95, hspace=0.45, wspace=0.3)

    for idx, (i, j) in enumerate(pairs):
        row = idx % n_rows
        col = idx // n_rows
        ax = fig.add_subplot(gs[row, col])

        sig_x = [ts_data[t]["clr"][i] for t in range(T)]
        sig_y = [ts_data[t]["clr"][j] for t in range(T)]
        freqs, H_mag, _, _ = compute_cross_spectrum(sig_x, sig_y)

        H_db = 20 * np.log10(np.maximum(H_mag[1:], 1e-15))
        ax.plot(freqs[1:], H_db, color=ACCENT_COLOR, linewidth=1.0)
        setup_axis(ax, f'{carriers[i]} → {carriers[j]}',
                   xlabel='Norm. Freq', ylabel='|H(f)| [dB]')

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page5_coherence(pdf, data):
    """Page 5: Coherence map — frequency-dependent correlation."""
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    ts_data = data["timesteps"]

    fig = new_page(pdf, 'COHERENCE MAP',
                   'gamma^2(f) = |<Sxy>|^2 / (<Sxx>*<Syy>) — Welch-averaged coherence')

    # Build coherence matrix at each frequency
    pairs = []
    for i in range(D):
        for j in range(i + 1, D):
            pairs.append((i, j))

    n_show = min(len(pairs), 6)
    n_rows = min(n_show, 3)
    n_cols = math.ceil(n_show / n_rows)
    gs = gridspec.GridSpec(n_rows, n_cols, top=0.88, bottom=0.06,
                           left=0.08, right=0.95, hspace=0.45, wspace=0.3)

    for idx in range(n_show):
        i, j = pairs[idx]
        row = idx % n_rows
        col = idx // n_rows
        ax = fig.add_subplot(gs[row, col])

        sig_x = [ts_data[t]["clr"][i] for t in range(T)]
        sig_y = [ts_data[t]["clr"][j] for t in range(T)]
        freqs, _, _, coherence = compute_cross_spectrum(sig_x, sig_y)

        ax.fill_between(freqs[1:], coherence[1:], alpha=0.3, color=ACCENT_COLOR)
        ax.plot(freqs[1:], coherence[1:], color=ACCENT_COLOR, linewidth=1.0)
        ax.axhline(y=0.5, color=WARN_COLOR, linewidth=0.5, linestyle='--',
                   alpha=0.5)
        ax.set_ylim(0, 1.05)
        setup_axis(ax, f'{carriers[i]} / {carriers[j]}',
                   xlabel='Norm. Freq', ylabel='Coherence')

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page6_group_delay(pdf, data):
    """Page 6: Group delay per carrier channel."""
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    ts_data = data["timesteps"]

    fig = new_page(pdf, 'GROUP DELAY',
                   'tau_g = -d(phase)/d(freq) — structural propagation delay')

    n_rows = min(D, 4)
    n_cols = math.ceil(D / n_rows)
    gs = gridspec.GridSpec(n_rows, n_cols, top=0.88, bottom=0.06,
                           left=0.08, right=0.95, hspace=0.45, wspace=0.3)

    for j in range(D):
        row = j % n_rows
        col = j // n_rows
        ax = fig.add_subplot(gs[row, col])
        signal = [ts_data[t]["clr"][j] for t in range(T)]
        freqs, _, phases = compute_fft(signal)
        gd = compute_group_delay(phases, freqs)

        c = CARRIER_COLORS[j % len(CARRIER_COLORS)]
        ax.plot(freqs[1:], gd[1:], color=c, linewidth=0.8)
        setup_axis(ax, carriers[j], xlabel='Norm. Freq',
                   ylabel='Group Delay [samples]')

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page7_impulse_response(pdf, data):
    """Page 7: Impulse response — autocorrelation of CLR channels."""
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    ts_data = data["timesteps"]

    fig = new_page(pdf, 'IMPULSE RESPONSE',
                   'Autocorrelation R(tau) via Wiener-Khinchin theorem')

    n_rows = min(D, 4)
    n_cols = math.ceil(D / n_rows)
    gs = gridspec.GridSpec(n_rows, n_cols, top=0.88, bottom=0.06,
                           left=0.08, right=0.95, hspace=0.45, wspace=0.3)

    for j in range(D):
        row = j % n_rows
        col = j // n_rows
        ax = fig.add_subplot(gs[row, col])
        signal = [ts_data[t]["clr"][j] for t in range(T)]
        autocorr = compute_autocorrelation(signal)
        lags = np.arange(len(autocorr))

        c = CARRIER_COLORS[j % len(CARRIER_COLORS)]
        ax.plot(lags, autocorr, color=c, linewidth=1.0)
        ax.axhline(y=0, color=GRID_COLOR, linewidth=0.5)
        # Confidence bounds (approximate 95% for white noise)
        conf = 1.96 / math.sqrt(T)
        ax.axhline(y=conf, color=WARN_COLOR, linewidth=0.3, linestyle='--')
        ax.axhline(y=-conf, color=WARN_COLOR, linewidth=0.3, linestyle='--')
        setup_axis(ax, carriers[j], xlabel='Lag', ylabel='R(tau)')

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page8_waterfall(pdf, data):
    """Page 8: Waterfall (spectrogram) — STFT of CLR channels."""
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    ts_data = data["timesteps"]

    fig = new_page(pdf, 'WATERFALL / SPECTROGRAM',
                   'Short-Time FFT — time-frequency decomposition of CLR channels')

    n_show = min(D, 4)
    gs = gridspec.GridSpec(n_show, 1, top=0.88, bottom=0.06,
                           left=0.08, right=0.92, hspace=0.40)

    for j in range(n_show):
        ax = fig.add_subplot(gs[j])
        signal = [ts_data[t]["clr"][j] for t in range(T)]
        times, freqs, stft_mag = compute_stft(signal)

        if stft_mag.size > 0 and stft_mag.shape[1] > 1:
            # Log magnitude for display
            log_mag = np.log10(np.maximum(stft_mag, 1e-15))
            ax.pcolormesh(times, freqs, log_mag,
                          cmap='inferno', shading='nearest')
        setup_axis(ax, carriers[j], xlabel='Time Index',
                   ylabel='Norm. Freq')

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page9_cepstrum(pdf, data):
    """Page 9: Real cepstrum — periodicity detection in spectrum."""
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    ts_data = data["timesteps"]

    fig = new_page(pdf, 'CEPSTRUM',
                   'IFFT(log|FFT|) — detects hidden periodicities in spectral domain')

    n_rows = min(D, 4)
    n_cols = math.ceil(D / n_rows)
    gs = gridspec.GridSpec(n_rows, n_cols, top=0.88, bottom=0.06,
                           left=0.08, right=0.95, hspace=0.45, wspace=0.3)

    for j in range(D):
        row = j % n_rows
        col = j // n_rows
        ax = fig.add_subplot(gs[row, col])
        signal = [ts_data[t]["clr"][j] for t in range(T)]
        cep = compute_cepstrum(signal)
        quefrency = np.arange(len(cep))

        c = CARRIER_COLORS[j % len(CARRIER_COLORS)]
        ax.plot(quefrency[1:], cep[1:], color=c, linewidth=0.8)
        setup_axis(ax, carriers[j], xlabel='Quefrency [samples]',
                   ylabel='Cepstral Amplitude')

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page10_vector_field(pdf, data):
    """Page 10: CLR velocity vector field + speed profile."""
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    ts_data = data["timesteps"]

    fig = new_page(pdf, 'VELOCITY VECTOR FIELD',
                   'CLR displacement vectors: v(t) = h(t+1) - h(t)')

    gs = gridspec.GridSpec(2, 1, top=0.88, bottom=0.06, left=0.08,
                           right=0.92, hspace=0.35)

    # Speed profile
    ax1 = fig.add_subplot(gs[0])
    setup_axis(ax1, 'CLR Speed Profile', ylabel='||v(t)|| [HLR/step]')
    speeds = []
    for t in range(T - 1):
        h0 = ts_data[t]["clr"]
        h1 = ts_data[t + 1]["clr"]
        speed = math.sqrt(sum((h1[j] - h0[j]) ** 2 for j in range(D)))
        speeds.append(speed)
    t_axis = np.arange(1, T)
    ax1.fill_between(t_axis, speeds, alpha=0.3, color=ACCENT_COLOR)
    ax1.plot(t_axis, speeds, color=ACCENT_COLOR, linewidth=1.5)

    # Per-carrier velocity components
    ax2 = fig.add_subplot(gs[1])
    setup_axis(ax2, 'Per-Carrier Velocity Components',
               xlabel='Time Index', ylabel='dh/dt [HLR/step]')
    for j in range(D):
        v_j = []
        for t in range(T - 1):
            v_j.append(ts_data[t + 1]["clr"][j] - ts_data[t]["clr"][j])
        c = CARRIER_COLORS[j % len(CARRIER_COLORS)]
        ax2.plot(t_axis, v_j, color=c, linewidth=0.8, alpha=0.8,
                 label=carriers[j])
    ax2.axhline(y=0, color=GRID_COLOR, linewidth=0.5)
    ax2.legend(fontsize=6, ncol=min(D, 4), loc='upper right',
               framealpha=0.3, facecolor=BG_COLOR, edgecolor=GRID_COLOR,
               labelcolor=FG_COLOR)

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page11_metric_evolution(pdf, data):
    """Page 11: Metric tensor trace + condition number evolution."""
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    ts_data = data["timesteps"]

    fig = new_page(pdf, 'METRIC TENSOR EVOLUTION',
                   'Higgins Steering Metric Tensor trace + condition number')

    gs = gridspec.GridSpec(3, 1, top=0.88, bottom=0.06, left=0.08,
                           right=0.92, hspace=0.35)
    t_axis = np.arange(T)

    # Trace
    ax1 = fig.add_subplot(gs[0])
    trace_vals = [ts_data[t]["metric_tensor_properties"]["trace"] for t in range(T)]
    ax1.semilogy(t_axis, trace_vals, color=ACCENT_COLOR, linewidth=1.5)
    setup_axis(ax1, 'Metric Tensor Trace: Tr(kappa^Hs)', ylabel='Tr(G) [log]')

    # Condition number
    ax2 = fig.add_subplot(gs[1])
    cond_vals = [ts_data[t]["metric_tensor_properties"]["condition_number"]
                 for t in range(T)]
    ax2.semilogy(t_axis, cond_vals, color=WARN_COLOR, linewidth=1.5)
    setup_axis(ax2, 'Condition Number: max(x)/min(x)', ylabel='kappa [log]')

    # Steering asymmetry
    ax3 = fig.add_subplot(gs[2])
    asym_vals = [ts_data[t]["metric_tensor_properties"]["asymmetry_ratio"]
                 for t in range(T)]
    ax3.semilogy(t_axis, asym_vals, color='#6bff6b', linewidth=1.5)
    setup_axis(ax3, 'Steering Asymmetry Ratio', xlabel='Time Index',
               ylabel='Ratio [log]')

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page12_summary(pdf, data):
    """Page 12: Navigation Summary Dashboard."""
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    ts_data = data["timesteps"]
    stats = data["global_statistics"]
    helm = data["helmsman_summary"]
    coroll = data["corollary_diagnostics"]

    fig = new_page(pdf, 'NAVIGATION SUMMARY',
                   f'{data["metadata"]["input_file"]} — {D} carriers x {T} steps')

    # Text dashboard
    ax = fig.add_axes([0.05, 0.05, 0.9, 0.85])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    lines = [
        ('SYSTEM IDENTIFICATION', '', True),
        ('Input', data["metadata"].get("input_file", "unknown")),
        ('Carriers (D)', f'{D}: {", ".join(carriers)}'),
        ('Timesteps (T)', f'{T} ({stats.get("hs_min", 0):.4f} to {stats.get("hs_max", 0):.4f} Hs)'),
        ('', ''),
        ('SPECTRAL SUMMARY', '', True),
        ('Hs Range', f'{stats["hs_range"]:.4f}'),
        ('Max Aitchison Dist', f'{stats["max_aitchison_distance"]:.4f} HLR'),
        ('Max Distance Pair', f'{stats.get("max_distance_pair", [])}'),
        ('Total Arc Length', f'{stats["total_arc_length"]:.4f} HLR'),
        ('Mean Angular Vel', f'{stats["mean_angular_velocity"]:.4f} deg/step'),
        ('Max Angular Vel', f'{stats["max_angular_velocity"]:.4f} deg/step'),
        ('', ''),
        ('HELMSMAN', '', True),
        ('Dominant', f'{helm["dominant_helmsman"]} ({helm["frequency"].get(helm["dominant_helmsman"], 0)}/{helm["total_transitions"]} steps)'),
        ('Frequency', str(helm["frequency"])),
        ('', ''),
        ('COROLLARY DIAGNOSTICS', '', True),
        ('Locked Pairs', f'{len(coroll["locks"])}'),
        ('Bearing Reversals', f'{len(coroll["reversals"])}'),
        ('', ''),
        ('INSTRUMENT', '', True),
        ('Engine', data["metadata"]["engine"]),
        ('Generated', data["metadata"]["generated"]),
    ]

    y = 0.95
    for item in lines:
        if len(item) == 3 and item[2]:
            # Section header
            ax.text(0.02, y, item[0], color=ACCENT_COLOR, fontsize=10,
                    fontweight='bold', fontfamily='monospace', va='top')
            y -= 0.035
        elif item[0] == '':
            y -= 0.015
        else:
            ax.text(0.04, y, f'{item[0]}:', color='#888888', fontsize=8,
                    fontfamily='monospace', va='top')
            ax.text(0.30, y, str(item[1]), color=FG_COLOR, fontsize=8,
                    fontfamily='monospace', va='top')
            y -= 0.030

    ax.text(0.5, 0.02,
            'The instrument reads. The expert decides. The loop stays open.',
            color='#555555', fontsize=7, ha='center', va='bottom',
            fontfamily='monospace', style='italic')

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════
# PAGE 13: Recursive Depth Sounding (requires depth JSON)
# ══════════════════════════════════════════════════════════════════

def page13_depth_sounding(pdf, data, depth_data):
    """Recursive depth tower visualization."""
    D = data["metadata"]["D"]
    carriers = data["metadata"]["carriers"]
    ds = depth_data["depth_summary"]

    fig = new_page(pdf, 'RECURSIVE DEPTH SOUNDING',
                   f'Energy depth={ds["energy_depth"]}, Curvature depth={ds["curvature_depth"]}, '
                   f'Max depth={ds["max_depth"]}')

    gs = gridspec.GridSpec(2, 2, figure=fig, left=0.08, right=0.95,
                           top=0.88, bottom=0.08, hspace=0.35, wspace=0.30)

    # Top-left: Energy Hs trajectory
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(BG_COLOR)
    e_traj = ds["energy_hs_trajectory"]
    ax1.plot(range(len(e_traj)), e_traj, '-o', color=ACCENT_COLOR,
             markersize=5, linewidth=1.5)
    ax1.set_xlabel('Level', color=FG_COLOR, fontsize=8)
    ax1.set_ylabel('Hs (mean)', color=FG_COLOR, fontsize=8)
    ax1.set_title('Energy Tower Hs Trajectory', color=FG_COLOR, fontsize=9)
    ax1.set_ylim(0, 1)
    ax1.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.5)
    ax1.tick_params(colors=FG_COLOR, labelsize=7)
    for spine in ax1.spines.values():
        spine.set_color(GRID_COLOR)
    ax1.text(0.5, 0.02, f'Depth: {ds["energy_depth"]} — {ds["energy_termination"]}',
             transform=ax1.transAxes, color=WARN_COLOR, fontsize=7,
             ha='center', fontfamily='monospace')

    # Top-right: Curvature Hs trajectory
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(BG_COLOR)
    c_traj = ds["curvature_hs_trajectory"]
    levels = range(len(c_traj))
    # Color even/odd differently to show period-2 cycle
    even_lvl = [i for i in levels if i % 2 == 0]
    even_hs = [c_traj[i] for i in even_lvl]
    odd_lvl = [i for i in levels if i % 2 == 1]
    odd_hs = [c_traj[i] for i in odd_lvl]
    ax2.plot(levels, c_traj, '-', color='#555555', linewidth=1)
    ax2.plot(even_lvl, even_hs, 'o', color=ACCENT_COLOR, markersize=5, label='Even')
    ax2.plot(odd_lvl, odd_hs, 's', color=WARN_COLOR, markersize=5, label='Odd')
    ax2.set_xlabel('Level', color=FG_COLOR, fontsize=8)
    ax2.set_ylabel('Hs (mean)', color=FG_COLOR, fontsize=8)
    ax2.set_title('Curvature Tower Hs Trajectory', color=FG_COLOR, fontsize=9)
    ax2.set_ylim(0, 1)
    ax2.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.5)
    ax2.tick_params(colors=FG_COLOR, labelsize=7)
    for spine in ax2.spines.values():
        spine.set_color(GRID_COLOR)
    ax2.legend(fontsize=6, loc='upper right', facecolor=BG_COLOR,
               edgecolor=GRID_COLOR, labelcolor=FG_COLOR)
    term = ds["curvature_termination"]
    ax2.text(0.5, 0.02, f'Depth: {ds["curvature_depth"]} — {term}',
             transform=ax2.transAxes, color=WARN_COLOR, fontsize=7,
             ha='center', fontfamily='monospace')

    # Bottom-left: Tower comparison bar chart
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(BG_COLOR)
    tower_names = ['Energy', 'Curvature']
    tower_depths = [ds["energy_depth"], ds["curvature_depth"]]
    bars = ax3.barh(tower_names, tower_depths, color=[ACCENT_COLOR, WARN_COLOR],
                    height=0.5, edgecolor='none')
    ax3.set_xlabel('Depth (levels)', color=FG_COLOR, fontsize=8)
    ax3.set_title('Tower Depth Comparison', color=FG_COLOR, fontsize=9)
    ax3.tick_params(colors=FG_COLOR, labelsize=8)
    for spine in ax3.spines.values():
        spine.set_color(GRID_COLOR)
    for bar, depth in zip(bars, tower_depths):
        ax3.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
                 str(depth), color=FG_COLOR, va='center', fontsize=9,
                 fontfamily='monospace')

    # Bottom-right: Involution proof summary
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(BG_COLOR)
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')

    inv = depth_data.get("involution_proof", {})
    info_lines = [
        ('METRIC DUAL INVOLUTION', '', True),
        ('M(x)_j', '(1/x_j) / sum(1/x_k)'),
        ('M^2 = I', f'residual: {inv.get("residual", 0):.2e}'),
        ('CLR negation', f'||clr(x)+clr(M(x))||: {inv.get("clr_negation_residual", 0):.2e}'),
        ('Duality dist', f'{inv.get("duality_distance", 0):.4f} HLR'),
        ('Verified', str(inv.get("verified", False))),
        ('', ''),
        ('CONVERGENCE', '', True),
        ('Precision', f'{ds.get("convergence_precision", 0.01)*100:.0f}%'),
        ('Energy rate', f'{ds["energy_convergence_rate"]:.6f} Hs/level'),
        ('Curvature rate', f'{ds["curvature_convergence_rate"]:.6f} Hs/level'),
        ('Duality dist', f'{ds["mean_duality_distance"]:.4f} HLR'),
    ]

    # Add cycle info
    c_cycle = ds.get("curvature_cycle", {})
    if c_cycle.get("detected"):
        info_lines.append(('Cycle', f'period-{c_cycle["period"]}, residual={c_cycle["residual"]:.2e}'))

    c_res = ds.get("curvature_residuals", {})
    if "attractor_even" in c_res:
        info_lines.append(('Attractor even', f'{c_res["attractor_even"]:.6f}'))
        info_lines.append(('Attractor odd', f'{c_res["attractor_odd"]:.6f}'))
        info_lines.append(('Amplitude', f'{c_res["attractor_amplitude"]:.6f}'))

    y = 0.95
    for item in info_lines:
        if len(item) == 3 and item[2]:
            ax4.text(0.02, y, item[0], color=ACCENT_COLOR, fontsize=9,
                     fontweight='bold', fontfamily='monospace', va='top')
            y -= 0.06
        elif item[0] == '':
            y -= 0.03
        else:
            ax4.text(0.04, y, f'{item[0]}:', color='#888888', fontsize=7,
                     fontfamily='monospace', va='top')
            ax4.text(0.45, y, str(item[1]), color=FG_COLOR, fontsize=7,
                     fontfamily='monospace', va='top')
            y -= 0.055

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page14_convergence_detail(pdf, data, depth_data):
    """Convergence characterization — residuals and attractor detail."""
    ds = depth_data["depth_summary"]

    fig = new_page(pdf, 'CONVERGENCE CHARACTERIZATION',
                   f'Curvature period-2 limit cycle — 1% precision target')

    gs = gridspec.GridSpec(2, 2, figure=fig, left=0.08, right=0.95,
                           top=0.88, bottom=0.08, hspace=0.35, wspace=0.30)

    c_traj = ds["curvature_hs_trajectory"]

    # Top-left: Same-parity convergence (even levels)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(BG_COLOR)
    even_vals = [c_traj[i] for i in range(0, len(c_traj), 2)]
    even_levels = list(range(0, len(c_traj), 2))
    ax1.plot(even_levels, even_vals, '-o', color=ACCENT_COLOR, markersize=5, linewidth=1.5)
    if len(even_vals) > 1:
        ax1.axhline(y=even_vals[-1], color=ACCENT_COLOR, linewidth=0.8, linestyle='--', alpha=0.5)
    ax1.set_xlabel('Level (even)', color=FG_COLOR, fontsize=8)
    ax1.set_ylabel('Hs (mean)', color=FG_COLOR, fontsize=8)
    ax1.set_title('Even-Parity Convergence', color=FG_COLOR, fontsize=9)
    ax1.set_ylim(0, 1)
    ax1.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.5)
    ax1.tick_params(colors=FG_COLOR, labelsize=7)
    for spine in ax1.spines.values():
        spine.set_color(GRID_COLOR)

    # Top-right: Same-parity convergence (odd levels)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(BG_COLOR)
    odd_vals = [c_traj[i] for i in range(1, len(c_traj), 2)]
    odd_levels = list(range(1, len(c_traj), 2))
    ax2.plot(odd_levels, odd_vals, '-s', color=WARN_COLOR, markersize=5, linewidth=1.5)
    if len(odd_vals) > 1:
        ax2.axhline(y=odd_vals[-1], color=WARN_COLOR, linewidth=0.8, linestyle='--', alpha=0.5)
    ax2.set_xlabel('Level (odd)', color=FG_COLOR, fontsize=8)
    ax2.set_ylabel('Hs (mean)', color=FG_COLOR, fontsize=8)
    ax2.set_title('Odd-Parity Convergence', color=FG_COLOR, fontsize=9)
    ax2.set_ylim(0, 1)
    ax2.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.5)
    ax2.tick_params(colors=FG_COLOR, labelsize=7)
    for spine in ax2.spines.values():
        spine.set_color(GRID_COLOR)

    # Bottom-left: Residual series (convergence rate)
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(BG_COLOR)
    if len(c_traj) >= 4:
        # Period-2 residuals: |Hs_k - Hs_{k-2}| for k >= 2
        p2_residuals = []
        p2_levels = []
        for k in range(2, len(c_traj)):
            res = abs(c_traj[k] - c_traj[k-2])
            p2_residuals.append(res)
            p2_levels.append(k)
        ax3.semilogy(p2_levels, p2_residuals, '-^', color='#6bff6b',
                     markersize=5, linewidth=1.5)
        # 1% threshold line
        threshold = ds.get("convergence_precision", 0.01)
        ax3.axhline(y=threshold, color=WARN_COLOR, linewidth=1, linestyle='--', alpha=0.7)
        ax3.text(p2_levels[-1], threshold * 1.5, f'{threshold*100:.0f}% threshold',
                 color=WARN_COLOR, fontsize=7, fontfamily='monospace', ha='right')
    ax3.set_xlabel('Level', color=FG_COLOR, fontsize=8)
    ax3.set_ylabel('|Hs_k - Hs_{k-2}|', color=FG_COLOR, fontsize=8)
    ax3.set_title('Period-2 Residual Decay', color=FG_COLOR, fontsize=9)
    ax3.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.5)
    ax3.tick_params(colors=FG_COLOR, labelsize=7)
    for spine in ax3.spines.values():
        spine.set_color(GRID_COLOR)

    # Bottom-right: Attractor phase portrait (even vs odd Hs)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(BG_COLOR)
    if len(c_traj) >= 3:
        # Plot Hs(k) vs Hs(k+1) — shows period-2 structure as 2-point orbit
        hs_k = c_traj[:-1]
        hs_k1 = c_traj[1:]
        ax4.plot(hs_k, hs_k1, '-o', color='#c0c0c0', markersize=4, linewidth=1,
                 alpha=0.7)
        # Mark start and end
        ax4.plot(hs_k[0], hs_k1[0], 'o', color=ACCENT_COLOR, markersize=8, zorder=5)
        ax4.plot(hs_k[-1], hs_k1[-1], 's', color=WARN_COLOR, markersize=8, zorder=5)
        # Identity line
        lim_min = min(min(hs_k), min(hs_k1)) * 0.9
        lim_max = max(max(hs_k), max(hs_k1)) * 1.1
        ax4.plot([lim_min, lim_max], [lim_min, lim_max], '--',
                 color=GRID_COLOR, linewidth=0.8)
    ax4.set_xlabel('Hs(k)', color=FG_COLOR, fontsize=8)
    ax4.set_ylabel('Hs(k+1)', color=FG_COLOR, fontsize=8)
    ax4.set_title('Return Map (Attractor Portrait)', color=FG_COLOR, fontsize=9)
    ax4.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.5)
    ax4.tick_params(colors=FG_COLOR, labelsize=7)
    for spine in ax4.spines.values():
        spine.set_color(GRID_COLOR)
    ax4.set_aspect('equal', adjustable='box')

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════
# MAIN: JSON → PDF
# ══════════════════════════════════════════════════════════════════

def run_analyzer(data, output_pdf, depth_data=None):
    """Generate complete spectral analysis PDF."""
    with PdfPages(output_pdf) as pdf:
        print("  Page 1:  System Overview (CLR + Hs + omega)")
        page1_overview(pdf, data)

        print("  Page 2:  Magnitude Spectrum (FFT power)")
        page2_magnitude_spectrum(pdf, data)

        print("  Page 3:  Phase Response (FFT phase)")
        page3_phase_response(pdf, data)

        print("  Page 4:  Transfer Function H(f)")
        page4_transfer_function(pdf, data)

        print("  Page 5:  Coherence Map (gamma^2)")
        page5_coherence(pdf, data)

        print("  Page 6:  Group Delay (tau_g)")
        page6_group_delay(pdf, data)

        print("  Page 7:  Impulse Response (autocorrelation)")
        page7_impulse_response(pdf, data)

        print("  Page 8:  Waterfall / Spectrogram (STFT)")
        page8_waterfall(pdf, data)

        print("  Page 9:  Cepstrum (periodicity detection)")
        page9_cepstrum(pdf, data)

        print("  Page 10: Velocity Vector Field")
        page10_vector_field(pdf, data)

        print("  Page 11: Metric Tensor Evolution")
        page11_metric_evolution(pdf, data)

        print("  Page 12: Navigation Summary")
        page12_summary(pdf, data)

        if depth_data is not None:
            print("  Page 13: Recursive Depth Sounding")
            page13_depth_sounding(pdf, data, depth_data)

            print("  Page 14: Convergence Characterization")
            page14_convergence_detail(pdf, data, depth_data)


def main():
    if len(sys.argv) < 2:
        print("Usage: python cnt_spectrum_analyzer.py engine_output.json [output.pdf] [--depth depth.json]")
        print("  engine_output.json: Output from cnt_tensor_engine.py")
        print("  output.pdf:         Spectral analysis plates (default: *_spectrum.pdf)")
        print("  --depth depth.json: Optional depth sounder JSON for pages 13-14")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = None
    depth_file = None

    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--depth' and i + 1 < len(sys.argv):
            depth_file = sys.argv[i + 1]
            i += 2
        elif output_file is None:
            output_file = sys.argv[i]
            i += 1
        else:
            i += 1

    if output_file is None:
        base = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base}_spectrum.pdf"

    print(f"CNT Compositional Spectrum Analyzer v2.0")
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    if depth_file:
        print(f"Depth:  {depth_file}")
    print()

    with open(input_file, 'r') as f:
        data = json.load(f)

    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    print(f"Carriers (D={D}): {', '.join(carriers)}")
    print(f"Timesteps (T={T}): {data['metadata']['labels'][0]} → {data['metadata']['labels'][-1]}")
    print(f"FFT resolution: {T} points → {T//2 + 1} frequency bins")
    print()

    # Load optional depth sounder data
    depth_data = None
    if depth_file:
        with open(depth_file, 'r') as f:
            depth_data = json.load(f)
        print(f"Depth sounder: max depth = {depth_data['depth_summary']['max_depth']}")
        print()

    print("Generating spectral plates...")
    run_analyzer(data, output_file, depth_data)
    print()

    page_count = 14 if depth_data else 12
    size_kb = os.path.getsize(output_file) / 1024
    print(f"Written: {output_file} ({size_kb:.1f} KB)")
    print(f"Pages: {page_count}")
    print()
    print("The instrument reads. The expert decides. The loop stays open.")


if __name__ == "__main__":
    main()
