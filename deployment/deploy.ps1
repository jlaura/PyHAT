conda deactivate;
conda config --set anaconda_upload yes;
Write-Host "Python Version: $args[ $1 ]"
conda build --token %CONDA_UPLOAD_TOKEN% --python $args[ $1 ] -c usgs-astrogeology recipe;
