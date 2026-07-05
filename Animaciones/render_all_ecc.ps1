param(
    [ValidateRange(0, 20)]
    [int]$SceneIndex = 0,
    [switch]$Still
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$miktex = "C:\Users\Enrique\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
if (Test-Path $miktex) {
    $env:Path = "$miktex;$env:Path"
}

$scenes = @(
    @{ File = "Video01_QueEsUnaCurvaEliptica.py"; Class = "QueEsUnaCurvaEliptica" },
    @{ File = "Video02_LeyDeGrupo.py"; Class = "LeyDeGrupo" },
    @{ File = "Video03_CasosEspeciales.py"; Class = "CasosEspeciales" },
    @{ File = "Video04_CamposFinitos.py"; Class = "CamposFinitos" },
    @{ File = "Video05_MultiplicacionEscalar.py"; Class = "MultiplicacionEscalar" },
    @{ File = "Video06_LogaritmoDiscreto.py"; Class = "LogaritmoDiscreto" },
    @{ File = "Video07_ECDH.py"; Class = "ECDH" },
    @{ File = "Video08_ECDSA.py"; Class = "ECDSA" },
    @{ File = "Video09_AtaquePollardsRho.py"; Class = "AtaquePollardsRho" },
    @{ File = "Video10_CurvasAnomalas.py"; Class = "CurvasAnomalas" },
    @{ File = "Video11_AtaqueSmart.py"; Class = "AtaqueSmart" },
    @{ File = "Video12_CanalLateralEnergia.py"; Class = "CanalLateralEnergia" },
    @{ File = "Video13_CurvasMontgomeryEdwards.py"; Class = "CurvasMontgomeryEdwards" },
    @{ File = "Video14_PairingsBilineales.py"; Class = "PairingsBilineales" },
    @{ File = "Video15_zkSNARKs.py"; Class = "ZkSNARKs" },
    @{ File = "Video16_AlgoritmoDeShor.py"; Class = "AlgoritmoDeShor" },
    @{ File = "Video17_CriptografiaDeIsogenias.py"; Class = "CriptografiaDeIsogenias" },
    @{ File = "Video18_GrafoDelMultiverso.py"; Class = "GrafoDelMultiverso" },
    @{ File = "Video19_AtaqueASIDH.py"; Class = "AtaqueASIDH" },
    @{ File = "Video20_ProtocolosModernosECC.py"; Class = "ProtocolosModernosECC" }
)

function Invoke-SceneRender {
    param(
        [Parameter(Mandatory = $true)]
        $Scene
    )

    $args = @("-m", "manim", "-r", "1280,720", "--fps", "30")
    if ($Still) {
        $args += "-s"
    }
    $args += @($Scene.File, $Scene.Class)
    & ..\.venv\Scripts\python.exe @args
}

if ($SceneIndex -eq 0) {
    foreach ($scene in $scenes) {
        Invoke-SceneRender -Scene $scene
    }
}
elseif ($SceneIndex -ge 1 -and $SceneIndex -le $scenes.Count) {
    Invoke-SceneRender -Scene $scenes[$SceneIndex - 1]
}
else {
    throw "SceneIndex must be 0 or between 1 and 20."
}
