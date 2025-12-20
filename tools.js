import { exec } from "child_process";

export function systemTool(cmd) {
  if (cmd.includes("shutdown"))
    exec("shutdown /s /t 0");

  if (cmd.includes("restart"))
    exec("shutdown /r /t 0");

  if (cmd.includes("sleep"))
    exec("rundll32.exe powrprof.dll,SetSuspendState 0,1,0");
}

export function appTool(cmd) {
  if (cmd.includes("calculator")) exec("calc");
  if (cmd.includes("notepad")) exec("notepad");
  if (cmd.includes("chrome")) exec("start chrome");
}
