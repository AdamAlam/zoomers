import { CardStack } from './ui/card-stack';

interface Props {
  // TODO Figure out the type to use here
  reviews: any[];
}

const ReviewStack = ({ reviews }: Props) => {
  return <CardStack items={reviews} />;
};
export default ReviewStack;
