import fetch from "node-fetch";
import dotenv from "dotenv";

dotenv.config();

export async function askJarvis(message) {
  const res = await fetch(
    `${process.env.OPENROUTER_BASE_URL}/chat/completions`,
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.OPENROUTER_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: process.env.OPENROUTER_MODEL,
        messages: [
          {
            role: "system",
            content:
              "You are JARVIS, Iron Man style AI assistant. Speak confidently, short, helpful, in Hindi or English."
          },
          { role: "user", content: message }
        ]
      })
    }
  );

  const data = await res.json();
  return data.choices[0].message.content;
}
