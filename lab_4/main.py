import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

plt.rcParams['toolbar'] = 'None'
plt.style.use('dark_background')

# Програма повинна мати початкові значення кожного параметру
start_amp = 1.0
start_freq = 2.0      
start_phase = 0.0
start_noise_mean = 0.0
start_noise_cov = 0.1
start_filter_cut = 5.0    

time_axis = np.linspace(0, 10, 1000)
sample_rate = 100  

stored_noise_data = np.random.normal(start_noise_mean, np.sqrt(start_noise_cov), len(time_axis))
prev_noise_config = (start_noise_mean, start_noise_cov)

# Реалізуйте функцію harmonic_with_noise
def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    global stored_noise_data, prev_noise_config
    
    if (noise_mean, noise_covariance) != prev_noise_config:
        stored_noise_data = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(time_axis))
        prev_noise_config = (noise_mean, noise_covariance)
        
    clean_signal = amplitude * np.sin(frequency * time_axis + phase)
    dirty_signal = clean_signal + stored_noise_data
    
    if show_noise:
        return clean_signal, dirty_signal
    else:
        return clean_signal, clean_signal

# Отриману гармоніку з накладеним на неї шумом відфільтруйте за допомогою фільтру на ваш вибір
def filter_signal(data, cut_freq, s_rate):
    nyq_freq = 0.5 * s_rate  
    norm_cut = cut_freq / nyq_freq
    
    if norm_cut >= 1.0: norm_cut = 0.99
    if norm_cut <= 0.0: norm_cut = 0.01
    
    coeff_b, coeff_a = butter(4, norm_cut, btype='low', analog=False)
    filtered_y = filtfilt(coeff_b, coeff_a, data)
    return filtered_y

# У програмі має бути створено головне вікно з такими елементами інтерфейсу Поле для графіка функції
main_fig, main_ax = plt.subplots(figsize=(10, 8))
main_fig.patch.set_facecolor('#1e1e1e') 
main_ax.set_facecolor('#252526')        
plt.subplots_adjust(left=0.1, bottom=0.55) 

init_clean, init_dirty = harmonic_with_noise(start_amp, start_freq, start_phase, start_noise_mean, start_noise_cov, True)
init_filtered = filter_signal(init_dirty, start_filter_cut, sample_rate)

plot_line_dirty, = main_ax.plot(time_axis, init_dirty, label="Зашумлена", color="#606060", alpha=0.8)
plot_line_clean, = main_ax.plot(time_axis, init_clean, label="Чиста", color="#00e5ff", linewidth=2)  
plot_line_filtered, = main_ax.plot(time_axis, init_filtered, label="Відфільтрована", color="#ff0055", linewidth=2, linestyle="--") 

main_ax.set_title("Інтерактивна гармоніка з шумом та фільтрацією", color="white")
main_ax.set_xlabel("Час (t)", color="lightgray")
main_ax.set_ylabel("Амплітуда (y)", color="lightgray")
main_ax.legend(loc='upper right', facecolor='#1e1e1e', edgecolor='#404040')
main_ax.grid(color='#404040', linestyle='--', linewidth=0.5)

# Слайдери які відповідають за амплітуду частоту гармоніки а також слайдери для параметрів шуму
bg_color_axes = '#333333' 
color_sl = '#007acc' 

axis_amp    = plt.axes([0.15, 0.45, 0.65, 0.03], facecolor=bg_color_axes)
axis_freq   = plt.axes([0.15, 0.40, 0.65, 0.03], facecolor=bg_color_axes)
axis_phase  = plt.axes([0.15, 0.35, 0.65, 0.03], facecolor=bg_color_axes)
axis_mean   = plt.axes([0.15, 0.30, 0.65, 0.03], facecolor=bg_color_axes)
axis_cov    = plt.axes([0.15, 0.25, 0.65, 0.03], facecolor=bg_color_axes)
axis_cutoff = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=bg_color_axes)

slider_amplitude = Slider(axis_amp, 'Амплітуда', 0.1, 10.0, valinit=start_amp, color=color_sl)
slider_frequency = Slider(axis_freq, 'Частота (ω)', 0.1, 20.0, valinit=start_freq, color=color_sl)
slider_phase     = Slider(axis_phase, 'Фаза (φ)', 0.0, 2*np.pi, valinit=start_phase, color=color_sl)
slider_n_mean    = Slider(axis_mean, 'Шум (Mean)', -2.0, 2.0, valinit=start_noise_mean, color=color_sl)
slider_n_cov     = Slider(axis_cov, 'Шум (Cov)', 0.0, 2.0, valinit=start_noise_cov, color=color_sl)
slider_cutoff    = Slider(axis_cutoff, 'Фільтр', 0.1, 20.0, valinit=start_filter_cut, color='#ff0055')

# Чекбокс для перемикання відображення шуму на гармоніці
axis_check = plt.axes([0.15, 0.05, 0.20, 0.10], facecolor=bg_color_axes)
chk_boxes = CheckButtons(axis_check, ['Шум', 'Фільтр'], [True, True])

for text_lbl in chk_boxes.labels:
    text_lbl.set_color('white')

# Кнопка Reset яка відновлює початкові параметри
axis_reset = plt.axes([0.40, 0.05, 0.20, 0.10])
button_reset = Button(axis_reset, 'Reset', color=bg_color_axes, hovercolor='#4d4d4d')
button_reset.label.set_color('white')

# Залиште інструкції для користувача які пояснюють як користуватися програмою
axis_info = plt.axes([0.65, 0.05, 0.20, 0.10])
button_info = Button(axis_info, 'Інструкція', color=color_sl, hovercolor='#005999')
button_info.label.set_color('white')

# Після оновлення параметрів програма повинна одразу оновлювати графік функції гармоніки з накладеним шумом
def refresh_plot(val=None):
    c_amp = slider_amplitude.val
    c_freq = slider_frequency.val
    c_phase = slider_phase.val
    c_mean = slider_n_mean.val
    c_cov = slider_n_cov.val
    c_cut = slider_cutoff.val
    
    is_noise_visible = chk_boxes.get_status()[0]
    is_filter_visible = chk_boxes.get_status()[1]

    new_clean, new_dirty = harmonic_with_noise(c_amp, c_freq, c_phase, c_mean, c_cov, is_noise_visible)
    
    plot_line_clean.set_ydata(new_clean)
    
    if is_noise_visible:
        plot_line_dirty.set_ydata(new_dirty)
        plot_line_dirty.set_visible(True)
    else:
        plot_line_dirty.set_visible(False)
        
    if is_filter_visible:
        new_filtered = filter_signal(new_dirty, c_cut, sample_rate)
        plot_line_filtered.set_ydata(new_filtered)
        plot_line_filtered.set_visible(True)
    else:
        plot_line_filtered.set_visible(False)
        
    main_fig.canvas.draw_idle()

slider_amplitude.on_changed(refresh_plot)
slider_frequency.on_changed(refresh_plot)
slider_phase.on_changed(refresh_plot)
slider_n_mean.on_changed(refresh_plot)
slider_n_cov.on_changed(refresh_plot)
slider_cutoff.on_changed(refresh_plot)
chk_boxes.on_clicked(refresh_plot)

# Після натискання кнопки Reset мають відновитись початкові параметри
def reset_params(event):
    slider_amplitude.reset()
    slider_frequency.reset()
    slider_phase.reset()
    slider_n_mean.reset()
    slider_n_cov.reset()
    slider_cutoff.reset()
    
    curr_status = chk_boxes.get_status()
    if not curr_status[0]:
        chk_boxes.set_active(0)
    if not curr_status[1]:
        chk_boxes.set_active(1)

# створення вікна інструкції
def display_help(event):
    info_window, info_axis = plt.subplots(figsize=(6, 3))
    info_window.patch.set_facecolor('#1e1e1e')
    info_axis.axis('off')
    
    help_text_content = (
        "ІНСТРУКЦІЯ КОРИСТУВАЧА:\n\n"
        "• Амплітуда, Частота, Фаза: змінюють форму чистої гармоніки.\n"
        "• Шум (Mean, Cov): генерують та налаштовують шум.\n"
        "• Фільтр: налаштовує частоту зрізу фільтра Баттерворта.\n"
        "• Чекбокси: вмикають/вимикають відображення відповідних ліній.\n"
        "• Reset: скидає всі налаштування до стандартних."
    )
    
    info_axis.text(0.5, 0.5, help_text_content, color='white', fontsize=12, 
                 ha='center', va='center', wrap=True)
    info_window.canvas.manager.set_window_title('Довідка')
    plt.show()

button_reset.on_clicked(reset_params)
button_info.on_clicked(display_help)

plt.show()