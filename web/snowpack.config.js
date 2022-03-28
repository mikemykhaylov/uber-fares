// Snowpack Configuration File
// See all supported options: https://www.snowpack.dev/reference/configuration

/** @type {import("snowpack").SnowpackUserConfig } */
module.exports = {
  mount: {
    /* ... */
    public: { url: '/', static: true },
    src: '/dist',
  },
  optimize: {
    minify: true,
    target: 'es2020',
    treeshake: true,
    splitting: true,
    sourcemap: 'external',
  },
  plugins: ['@snowpack/plugin-react-refresh', '@snowpack/plugin-typescript'],
  packageOptions: {
    knownEntrypoints: ['mapbox-gl']
    /* ... */
  },
  devOptions: {
    /* ... */
  },
  buildOptions: {
    /* ... */
  },
};
