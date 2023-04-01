import h5py

# open the h5 file
with h5py.File('/model.h5', 'r') as f:
    # create a new h5 file with compression enabled
    with h5py.File('compressed_file.h5', 'w') as f_comp:
        # iterate over the datasets in the original file
        for name in f:
            # copy each dataset to the new file with compression
            f.copy(name, f_comp[name], name=name, swmr=True, deflate=4, shuffle=True)
