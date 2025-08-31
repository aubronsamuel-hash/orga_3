Param()
$env:E2E_ACCEPTANCE = "1"
pwsh -NoLogo -NoProfile -c "pushd frontend; npm ci; npm run build --if-present; npm run e2e; popd"
