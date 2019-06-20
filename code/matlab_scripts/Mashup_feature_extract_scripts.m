%% "Mashup_feature_extract_scripts.m" is used to extract drug features from seven drug networks.

svd_approx = true;  % use SVD approximation for Mashup
ndimlist=[700]      %   dimension of compact feature.

%% Construct network file paths
string_nets = {'chempair1', 'chempair2', 'chempair3', 'chempair4', 'chempair5','chempair6','chempair7'};

network_files = cell(1, length(string_nets));
for i = 1:length(string_nets)
    network_files{i} = sprintf('../data/Mashup_input_file/%s_adjacency.txt',string_nets{i});
end

%% Load gene list
gene_file = sprintf('../data/Mashup_input_file/drugs.txt');
genes = textread(gene_file, '%s');
ngene = length(genes);
for i=1:length(ndimlist)
%% Mashup integration and feature extraction.
    ndim=ndimlist(i);
    fprintf('[Mashup]\n');
    x = mashup(network_files, ngene, ndim, svd_approx);
    path2=['../data/Mashup_output_file/drug3883_'  num2str(ndim)  '.csv']
    csvwrite(path2,x);
end
