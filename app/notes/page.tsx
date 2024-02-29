import { createClient } from "@/utils/supabase/server";

export default async function Page() {
  const supabase = createClient();

  const { data: notes } = await supabase.from("notes").select();
  console.log(notes);
  return (
    <ul>
      {notes?.map((note) => (
        <li key={note.id}>{note.title}</li>
      ))}
    </ul>
  );
}
