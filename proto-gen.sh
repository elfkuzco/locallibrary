#!/bin/bash

service_name=$1
release_version=$2
language=$3


gen_python_package() {
    # Install the gRPC tools
    python3 -m pip install --upgrade pip
    python3 -m pip install grpcio
    python3 -m pip install grpcio-tools

    # Create the directory for putting the stubs
    package_name="locallibrary_${service_name}_grpc"
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
    # Delete non-generated files
    delete_non_generated_files "$package_name"
    # Move the generated files to the root
    mv "$package_name"/* .

    commit_release
}

delete_non_generated_files () {
    local generated=$1
    # shellcheck disable=SC2086
    # shellcheck disable=SC2038
    find . -mindepth 1 -maxdepth 1 -not \( -path ./.git -prune \) -not \( -path ./$generated -prune \) | xargs rm -rf
}

gen_golang_package() {
    # Install the gRPC tools
     #sudo apt-get install -y protobuf-compiler
     #go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
     #go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
    # shellcheck disable=SC2155
    #export PATH="$PATH:$(go env GOPATH)/bin"

    module_root="github.com/elfkuzco/locallibrary"
    dest="grpc/golang/${service_name}"
    module_name="${module_root}/${dest}"

    protoc --go_out=. --go_opt=module="$module_root" \
	--go-grpc_out=. --go-grpc_opt=module="$module_root" \
	./proto/"${service_name}"/*.proto

    pushd .
    cd "$dest" || { echo "error switching to $dest directory."; exit 1; }
    go mod init "$module_name"
    go mod tidy
    popd || { echo "error switching to project root."; exit 1; }

    delete_non_generated_files "grpc"

    commit_release
}

commit_release() {
    git config --global user.email "orjiuchechukwu52@yahoo.com"
    git config --global user.name "Orji Uchechukwu"
    # Include the generated files and commit to a new tag
    git add . && git commit -m "${language} grpc stubs for ${service_name} ${release_version}"
    git tag -fa "grpc/${language}/${service_name}/${release_version}" \
	-m "grpc/${language}/${service_name}/${release_version}"
    git push origin -f "refs/tags/grpc/${language}/${service_name}/${release_version}"
}

if [[ "$language" = "golang" ]]; then
    gen_golang_package
elif [[ "$language" = "python" ]]; then
    gen_python_package
else
    echo "Generation logic not implemented for language ${language}"
    exit 1
fi
