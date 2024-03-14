'use client';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from '@/components/ui/card';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { useToast } from '@/components/ui/use-toast';
import axios from 'axios';
import Image from 'next/image';
import { useEffect, useState } from 'react';
import { Movie } from '../../movie.types';

interface FormData {
  reviewText: string;
  stars: number;
  mediaId: string;
  user: number;
}

const MovieDetail = ({ params }: { params: { movieId: string } }) => {
  const { toast } = useToast();
  const [movieDetails, setMovieDetails] = useState<Movie>();
  const imageUrl = 'https://image.tmdb.org/t/p/original';
  const [formData, setFormData] = useState<FormData>({
    reviewText: '',
    stars: 2.5,
    mediaId: params.movieId,
    user: 1
  });

  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  useEffect(() => {
    if (params.movieId !== undefined) {
      fetch(`http://localhost:8000/movie/${params.movieId}}`)
        .then(res => res.json())
        .then(data => setMovieDetails(data));
    }
  }, [params.movieId]);

  const handleReviewSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    axios
      .post(`http://localhost:8000/reviews`, {
        MediaId: params.movieId,
        stars: 5,
        ReviewText: formData.reviewText || '',
        User: 1
      })
      .then(res => {
        if (res.status === 200) {
          toast({
            title: 'Review Submitted',
            description: `Your review for ${movieDetails?.title} been submitted`,
            duration: 5000
          });
        }
      })
      .catch(err => {
        toast({
          variant: 'destructive',
          title: 'Error',
          description:
            'There was an error submitting your review. You may have already submitted a review for this film.'
        });
      });
  };

  return movieDetails ? (
    <div className="mx-auto max-w-screen-lg">
      <div className="flex flex-col items-center justify-center">
        <div className="relative mb-4 h-[500px] w-full">
          <Image
            src={`${imageUrl}${movieDetails.backdrop_path}`}
            layout="fill"
            objectFit="cover"
            alt="Movie backdrop image"
          />
          {/* Overlay for bottom fade */}
          <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-white to-transparent" />

          {/* Overlay for left side fade
          <div className="absolute bottom-0 left-0 top-0 w-32 bg-gradient-to-r from-white to-transparent" />
          {/* Overlay for right side fade */}
          {/* <div className="absolute bottom-0 right-0 top-0 w-32 bg-gradient-to-l from-white to-transparent" /> */}
        </div>
        <div className="flex w-full justify-start">
          <div className="mr-8 shrink-0">
            <Image
              src={`${imageUrl}${movieDetails.poster_path}`}
              alt={movieDetails.title}
              width={200}
              height={300}
              style={{ borderRadius: '10px' }}
            />
          </div>
          <div>
            <h1 className="mb-2 font-serif text-3xl">{movieDetails.title}</h1>
            <p className="mb-2 text-sm uppercase">{movieDetails.tagline}</p>
            <p className="mr-4">{movieDetails.overview}</p>
          </div>
          <div className="flex min-h-[300px] min-w-[350px]">
            <Card className="grow-1 w-full">
              <CardHeader>
                <CardTitle>Add A Review</CardTitle>
                <CardDescription>
                  Create new review for {movieDetails.title}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleReviewSubmit}>
                  <Textarea
                    placeholder="Leave a Review Here"
                    onChange={handleFormChange}
                    name="reviewText"
                    className="mb-4 w-full"
                  />
                  {/* //TODO: I will make a custom stars component eventually */}
                  <Select
                    onValueChange={e => {
                      setFormData({ ...formData, stars: parseFloat(e) });
                    }}
                    name="stars"
                    defaultValue={formData.stars.toString()}
                  >
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Rating" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="0.5">0.5</SelectItem>
                      <SelectItem value="1">1</SelectItem>
                      <SelectItem value="1.5">1.5</SelectItem>
                      <SelectItem value="2">2</SelectItem>
                      <SelectItem value="2.5">2.5</SelectItem>
                      <SelectItem value="3">3</SelectItem>
                      <SelectItem value="3.5">3.5</SelectItem>
                      <SelectItem value="4">4</SelectItem>
                      <SelectItem value="4.5">4.5</SelectItem>
                      <SelectItem value="5">5</SelectItem>
                    </SelectContent>
                  </Select>
                  <Button type="submit" className="mt-4">
                    Submit New Review
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  ) : (
    <div>Loading...</div>
  );
};

export default MovieDetail;
