#!/bin/bash

service_name=$1
release_version=$2

# Install the gRPC tools
python3 -m pip3 install --upgrade pip
python3	-m pip install grpcio
python3 -m pip install grpcio-tools

package_name="locallibrary_${service_name}_grpc"

# Create the directory for putting the stubs
dest="${package_name}/src"
mkdir -p "$dest"

# Generate the stubs to the proper location with the package_name
python3 -m grpc_tools.protoc -I"${package_name}"="./proto/${service_name}" \
    --python_out="$dest" --grpc_python_out="$dest" --pyi_out="$dest" \
    ./proto/"${service_name}"/*.proto

# Create the __init__ file so the directory under src is a valid Python
# module
touch "${package_name}/src/${package_name}/__init__.py"

# Generate the pyproject.toml file and place it inside the root of the package directory
cat << EOF > "${package_name}/pyproject.toml"
[build-system]
requires = ["setuptools >= 61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "$package_name"
description = "Locallibrary Frontend Python gRPC stubs"
requires-python = ">=3.11"
version = "${release_version#v}"
dependencies = [
    "$(pip3 freeze | grep grpcio==)",
    "$(pip3 freeze | grep protobuf==)",
]
EOF

git config --global user.email "orjiuchechukwu52@yahoo.com"
git config --global user.name "Orji Uchechukwu"

# Delete non-generated files
find . -mindepth 1 -maxdepth 1 -not \( -path ./.git -prune \) -not \( -path ./$package_name -prune \) | xargs rm -rf
# Move the generated files to the root
mv $package_name/* .

# Include the generated files and commit to a new tag
git add . && git commit -m "python grpc stubs for ${service_name} ${release_version}" || true
git tag -fa "python/${service_name}/${release_version}" \
    -m "python/${service_name}/${release_version}"
git push origin -f "refs/tags/python/${service_name}/${release_version}"
