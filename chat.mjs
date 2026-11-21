const apiKey = process.env.HEX_API_KEY;

if (!apiKey) {
  console.error("Set HEX_API_KEY before running this example.");
  process.exit(1);
}

const model = process.argv[2] ?? "glm-5.3-abliterated";

try {
  const response = await fetch("https://api.hexapi.io/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: "user", content: "Explain why a development server uses a local port." },
      ],
      max_tokens: 256,
    }),
    signal: AbortSignal.timeout(90_000),
  });

  if (!response.ok) {
    throw new Error(`HEX returned HTTP ${response.status}. See https://hexapi.io/docs for help.`);
  }

  const completion = await response.json();
  console.log(completion.choices[0].message.content || "(No text returned)");
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
