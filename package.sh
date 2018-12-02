# build package into the wheel as below:
# dist/
#   pyx3-0.0.1-py3-none-any.whl
#   pyx3-0.0.1.tar.gz

python3 setup.py sdist bdist_wheel

# twine upload dist/* to upload your package, and you should see output similar to this:
# Uploading distributions to https://test.pypi.org/legacy/
# Enter your username: [your username]
# Enter your password:
# Uploading pyx3-0.0.1-py3-none-any.whl
# 100%|█████████████████████| 4.65k/4.65k [00:01<00:00, 2.88kB/s]
# Uploading pyx3-0.0.1.tar.gz
# 100%|█████████████████████| 4.25k/4.25k [00:01<00:00, 3.05kB/s]
twine upload dist/*


# pipreqs x3 to see package dependencies
# pipreqs x3