conda deactivate;
conda config --set anaconda_upload yes;
conda build --token %CONDA_UPLOAD_TOKEN% --python $args[ $1 ] -c usgs-astrogeology recipe;
