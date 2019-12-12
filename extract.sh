# Extract benchmark 
echo "Extracting raw benchmark from tar..."
tar xzf ./benchmark/UTAnLay.tar.gz -C ./benchmark/ --strip 1
rm ./benchmark/*.sp

# Extract placement feature images
echo "Begin feature image extraction."
python extract_feature.py
