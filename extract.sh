# Extract benchmark 
echo "Extracting raw benchmark from tar..."
tar xzf ./benchmark/UTAnLay.tar.gz -C ./benchmark/ --strip 1
rm ./benchmark/*.sp

# Extract dataset to ./data
echo "Begin feature image extraction."
rm ./data/*
python extract_feature.py
