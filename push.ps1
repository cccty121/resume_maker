# 授权完成后跑这个：推送 + 验收
$env:PATH='D:\devtools\MinGit\cmd;'+$env:PATH
$env:GIT_TERMINAL_PROMPT='0'
cd 'D:\work\resume_maker'

Write-Host '--- who am I ---'
& 'D:\devtools\gh\gh.exe' auth status 2>&1 | Select-Object -First 6

Write-Host '--- push ---'
git -c http.proxy=http://127.0.0.1:7897 push -u origin main 2>&1 | Select-Object -Last 6

Write-Host '--- pages enable ---'
& 'D:\devtools\gh\gh.exe' api -X POST "repos/cccty121/resume_maker/pages" -f "source[branch]=main" -f "source[path]=/" 2>&1 | Select-Object -First 6

Write-Host '--- wait for pages ---'
Start-Sleep -Seconds 60

Write-Host '--- verify ---'
foreach ($s in 'eng','sci','arts','soc') {
  python D:\work\resume_create\tools\verify_site.py --base "https://cccty121.github.io/resume_maker/$s/" --expect-qr "https://cccty121.github.io/resume_maker/$s/" 2>&1 | Select-Object -Last 4
}
