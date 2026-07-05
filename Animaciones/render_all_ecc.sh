#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

SCENE_INDEX="${1:-0}"

FILES=(
  "Video01_QueEsUnaCurvaEliptica.py:QueEsUnaCurvaEliptica"
  "Video02_LeyDeGrupo.py:LeyDeGrupo"
  "Video03_CasosEspeciales.py:CasosEspeciales"
  "Video04_CamposFinitos.py:CamposFinitos"
  "Video05_MultiplicacionEscalar.py:MultiplicacionEscalar"
  "Video06_LogaritmoDiscreto.py:LogaritmoDiscreto"
  "Video07_ECDH.py:ECDH"
  "Video08_ECDSA.py:ECDSA"
  "Video09_AtaquePollardsRho.py:AtaquePollardsRho"
  "Video10_CurvasAnomalas.py:CurvasAnomalas"
  "Video11_AtaqueSmart.py:AtaqueSmart"
  "Video12_CanalLateralEnergia.py:CanalLateralEnergia"
  "Video13_CurvasMontgomeryEdwards.py:CurvasMontgomeryEdwards"
  "Video14_PairingsBilineales.py:PairingsBilineales"
  "Video15_zkSNARKs.py:ZkSNARKs"
  "Video16_AlgoritmoDeShor.py:AlgoritmoDeShor"
  "Video17_CriptografiaDeIsogenias.py:CriptografiaDeIsogenias"
  "Video18_GrafoDelMultiverso.py:GrafoDelMultiverso"
  "Video19_AtaqueASIDH.py:AtaqueASIDH"
  "Video20_ProtocolosModernosECC.py:ProtocolosModernosECC"
)

render_scene() {
  local entry="$1"
  local file="${entry%%:*}"
  local klass="${entry##*:}"
  python -m manim -r 1280,720 --fps 30 "$file" "$klass"
}

if [[ "$SCENE_INDEX" == "0" || "$SCENE_INDEX" == "all" ]]; then
  for entry in "${FILES[@]}"; do
    render_scene "$entry"
  done
else
  if ! [[ "$SCENE_INDEX" =~ ^[0-9]+$ ]] || (( SCENE_INDEX < 1 || SCENE_INDEX > ${#FILES[@]} )); then
    echo "Scene index must be 0, all, or a number between 1 and 20." >&2
    exit 1
  fi
  render_scene "${FILES[$((SCENE_INDEX - 1))]}"
fi
