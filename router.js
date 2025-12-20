export function routeTask(text) {
  text = text.toLowerCase();

  if (["shutdown", "restart", "sleep"].some(x => text.includes(x)))
    return "system";

  if (["open", "calculator", "notepad", "chrome"].some(x => text.includes(x)))
    return "app";

  return "ai";
}
