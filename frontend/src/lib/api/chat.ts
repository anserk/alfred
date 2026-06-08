import { z } from "zod";

export async function postMessageAsync(userMessage: string) {
  const res = await fetch("/api/chat/stream", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userMessage }),
  });

  if (!res.ok || !res.body) throw new Error("Stream unavailable");
  return res.body.getReader();
}

export const TopicDtoSchema = z.object({
  id: z.uuid(),
  title: z.string(),
  summary: z.string().nullable().optional(),
});

export type TopicDto = z.infer<typeof TopicDtoSchema>;
export const TopicDtoListSchema = z.array(TopicDtoSchema);
export type TopicDtoList = z.infer<typeof TopicDtoListSchema>;
export async function getTopicsAsync(): Promise<TopicDtoList> {
  const res = await fetch("/api/topics", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!res.ok || !res.body) throw new Error("Error.");
  var parsed = await TopicDtoListSchema.safeParseAsync(await res.json());
  if (parsed.error) {
    throw new Error("Unable to parse response from server.");
  }

  return parsed.data;
}

// export const getCurrentTitleSchema = z.object({
//   title: z.string(),
// });
// export const getCurrentTitle = async (fetchFn: typeof fetch) => {
//   const res = await fetchFn(" http://backend:8000/chat/getTitle", {
//     method: "GET",
//     headers: {
//       "Content-Type": "application/json",
//     },
//   });

//   if (!res.ok || !res.body) throw new Error("Cannot talk to BE.");
//   const parsed = await getCurrentTitleSchema.safeParseAsync(await res.json());

//   if (!parsed.success) {
//     throw new Error("Unable to parse response.");
//   }

//   return parsed.data;
// };
