/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'image.tmdb.org',
      },
      // TODO: Remove when not needed. Currently used as placeholder image for reviewer profile pictures.
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
      },
      // TODO: Remove when profile picture source is finalized
      //  Temporary - for profile images being sourced from multiple places
      {
        protocol: 'https',
        hostname: 'avatars.githubusercontent.com',
      },
      {
        protocol: 'https',
        hostname: 'cloudflare-ipfs.com',
      },
    ],
  },
};

export default nextConfig;
