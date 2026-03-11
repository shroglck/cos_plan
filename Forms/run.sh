
function downloadTxtFile(filename, content) {
    const blob = new Blob([content], { type: "text/plain;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}


function remove_elements(questions) {
    const results = [];

    questions.forEach(element => {
        const  p = element.querySelector("p");
        const text = (p?.textContent || "").replace(/\s+/g, " ").trim();
        const match = text.match(/\(Q\d+:\s*\d+\s*\/\s*\d+\)/);
        const qStr = match ? match[0] : null;
        console.log(qStr)
        if (qStr) {
            results.push(qStr);
        }
    });
    const txt = results.join("\n");  // all strings combined
    console.log(txt);
    return txt;

}
const txt = remove_elements(questions_robo);
downloadTxtFile("robo_map.txt", txt);

const txt = remove_elements(questions_maze);
downloadTxtFile("maze_map.txt", txt);





# cd ~/Downloads/Submission/"CosPlan (Shresth) CVPR'26"/cos_plan/Forms/

import sys, os 
current_path = os.getcwd()
sys.path.append(os.path.join(current_path, "plot"))
from plot.line import line_plot
from plot.colors import *

X = [0, 1, 2, 3]
X_labels = ['[0]', '[n/3]', '[n/2]', '[n]']
Lines = [ 
    (X, [23.4, 23.5, 23.8, 25.2]), 
    (X, [41.2, 38.8, 41.1, 43.2]), 
]

X = [1, 2, 3]
X_labels = ['[n/3]', '[n/2]', '[n]']
Lines = [ 
    (X, [23.5, 23.8, 25.2]), 
    (X, [38.8, 41.1, 43.2]), 
]


plot_config = dict(
    figsize=(8, 5), artificial_darkening=0.85,
    line_width=5, alpha_line=1, decimal_places=0,
    y_padding_factor=-0.0, y_points=2, Y_label_fontsize=25, y_up_offset=2, y_down_offset=2,
    X_labels=X_labels, X_labels_pos = X, X_label_fontsize=25, x_padding_factor=-0.04, x_padding=0.08,
    use_scatter=True, scatter_size=300,
    grid_opacity=1, grid_shape='x',
)

line_plot(Lines, name="n_steps", COLORS=DISTINCT_2_2, **plot_config)
    
    

# shuffle
# internvlm_sgi_n/3	0.235
# internvlm_sgi_n/2	0.238
# internvlm_sgi n 25.2
# SG 23.4

# Maze 
# Internvlm_SGI_n/2		0.411
# InternVlm_SGI_n/3		0.388
# SGI 43.2
# SG 41.2





# shuffle K Steps into the future																									
K = [2,3,5,7,9]
Internvlm3_cot =  [42.04, 44.4, 45.6, 42.6, 44.8]
Internvlm3_sgi =  [41.3,  43.5, 44.3,  47.5, 50.5]

qwen3_cot  =      [33.4, 35.3, 37.2, 33.1, 32.4]
qwen3_sgi  =      [37.3, 35.3, 42.1, 36.3, 39.6]

name = 'maze_k_step_into_future'
max_limit = 52

X = K
X_labels= [str(e) for e in X]


Lines = [
    [X, Internvlm3_cot],  
    [X, Internvlm3_sgi],
    [X, qwen3_cot], 
    [X, qwen3_sgi],
]

y_up_offset = max_limit - max([max(e[1]) for e in Lines])
y_down_offset = min([min(e[1]) for e in Lines])
y_down_offset=10

line_plot(Lines, COLORS=[LIGHT_DARK_PAIR[10], LIGHT_DARK_PAIR[11], LIGHT_DARK_PAIR[4], LIGHT_DARK_PAIR[5]],
figsize=(8, 6), name="test_multiple", artificial_darkening=0.95,
decimal_places=0, y_up_offset=y_up_offset, y_down_offset=y_down_offset, Y_label_fontsize=25, 
x_down_offset=0, y_padding_factor=-0.0, y_points=2, 
X_labels=X_labels, X_labels_pos = X, X_label_fontsize=25, x_padding_factor=-0.04, x_padding=0.1,
scatter_size=300, grid_shape='both', 
h_lines=[20], h_line_alpha=1, hline_color='black', hline_style="-", )






from plot.hist import bar_graph_side_by_side

# shuffle K Steps into the future																									
X = ['InternVLM-2',  'Qwen 3', 'InternVLM-3', 'Janus', 'CoG-VLM']
Hists = [
        [43, 35, 41, 23, 27],
        [39, 30, 35, 22, 23],
    ]
bar_graph_side_by_side(Hists, name="cheating_models", COLORS=DISTINCT_2_2,
artificial_darkening=1, decimal_places=0, barWidth=0.4, gap_between_bars=0.5,  gap_between_groups=1,
figsize=(12, 6),  x_ticks_allowed=False, bar_opacity=1,  
y_points=5, Y_label_fontsize=25, y_up_offset=1, y_down_offset=10, y_padding_factor=-0.03, switch_off_yaxis=True, 
x_padding_factor=-0.1, x_padding=-0.09, 
)





Internvlm2_cot =  [42.04, 44.4, 45.6, 42.6, 44.8]
Internvlm3_sgi =  [41.3,  43.5, 44.3,  47.5, 50.5]

qwen3_cot  =      [33.4, 35.3, 37.2, 33.1, 32.4]
qwen3_sgi  =      [37.3, 35.3, 42.1, 36.3, 39.6]

name = 'maze_k_step_into_future'
max_limit = 52

X = K
X_labels= [str(e) for e in X]


Lines = [
    [X, Internvlm3_cot],  
    [X, Internvlm3_sgi],
    [X, qwen3_cot], 
    [X, qwen3_sgi],
]

y_up_offset = max_limit - max([max(e[1]) for e in Lines])
y_down_offset = min([min(e[1]) for e in Lines])
y_down_offset=10

line_plot(Lines, COLORS=[LIGHT_DARK_PAIR[10], LIGHT_DARK_PAIR[11], LIGHT_DARK_PAIR[4], LIGHT_DARK_PAIR[5]],
figsize=(8, 6), name="test_multiple", artificial_darkening=0.95,
decimal_places=0, y_up_offset=y_up_offset, y_down_offset=y_down_offset, Y_label_fontsize=25, 
x_down_offset=0, y_padding_factor=-0.0, y_points=2, 
X_labels=X_labels, X_labels_pos = X, X_label_fontsize=25, x_padding_factor=-0.04, x_padding=0.1,
scatter_size=300, grid_shape='both', 
h_lines=[20], h_line_alpha=1, hline_color='black', hline_style="-", )



