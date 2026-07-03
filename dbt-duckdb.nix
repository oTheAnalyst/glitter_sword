{
  lib,
  python3Packages,
  python313Packages,
  fetchFromGitHub,
}:
python3Packages.buildPythonPackage rec {
  pname = "dbt-duckdb";
  version = "1.10.1";
  pyproject = true;

  src = fetchFromGitHub {
    owner = "duckdb";
    repo = "dbt-duckdb";
    tag = version;
    hash = "sha256-Xqd2u2x0rPfPwFYNDJPvQzCNyDa9TpmdSWQLyKRMLtk=";
  };

  env.PBR_VERSION = version;

  build-system = with python313Packages; [
    setuptools
    pbr
  ];

  dependencies = with python313Packages; [
    dbt-adapters
    dbt-common
    duckdb
    dbt-core
  ];

  # tests exist for the dbt tool but not for this package specifically
  doCheck = false;

  ##  pythonImportsCheck = ["dbt.adapters.duckdb"];

  meta = {
    description = "Plugin enabling dbt to work with a Duckdb database";
    homepage = "https://github.com/duckdb/dbt-duckdb/";
    license = lib.licenses.asl20;
  };
}
