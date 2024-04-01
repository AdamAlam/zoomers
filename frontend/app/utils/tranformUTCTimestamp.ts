// Provided UTC timestamp
export const transformTimestamp = (timestampStr: string) => {
  const date = new Date(timestampStr);

  const options: Intl.DateTimeFormatOptions = {
    month: 'short',
    day: 'numeric'
  };
  const formattedLocalTime = date.toLocaleDateString('en-US', options);

  return formattedLocalTime;
};
