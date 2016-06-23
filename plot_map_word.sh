cat input | python determine_region.py -g precompute/grid_region | awk -F '\t' '{print $3}' | sort -k1,1n | uniq -c | awk '{print $2 "\t" $1}' | python plot_word_region.py "exemple"
