/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://backend:8000/api/:path*',
      },
      {
        source: '/ai/:path*',
        destination: 'http://ai-service:5000/:path*',
      },
    ]
  },
}

module.exports = nextConfig
