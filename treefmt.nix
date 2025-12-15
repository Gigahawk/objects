{ pkgs, ... }:
{
  projectRootFile = "flake.nix";
  programs.black.enable = true;
  programs.nixfmt.enable = true;
  programs.actionlint.enable = true;
  programs.yamlfmt.enable = true;
}
