'use client';
import { useState } from 'react';
import { Input } from './ui/input';
import axios from 'axios';
import { useRouter } from 'next/navigation';

interface Props {}
function MovieSearch({}: Props) {
  const [search, setSearch] = useState('');
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    router.push(`/search/${encodeURI(search)}`);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <Input
          placeholder="Search for a movie"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
      </form>
    </div>
  );
}
export default MovieSearch;
