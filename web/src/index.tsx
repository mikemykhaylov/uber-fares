import React from 'react';
import { render } from 'react-dom';
import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import { RecoilRoot } from 'recoil';
import App from './containers/App';

const theme = extendTheme({
  styles: {
    global: {
      body: {
        bg: 'gray.100',
        pb: '4rem',
      },
    },
  },
});

render(
  <React.StrictMode>
    <RecoilRoot>
      <ChakraProvider theme={theme}>
        <App />
      </ChakraProvider>
    </RecoilRoot>
  </React.StrictMode>,
  document.getElementById('root'),
);

// Hot Module Replacement (HMR) - Remove this snippet to remove HMR.
// Learn more: https://www.snowpack.dev/concepts/hot-module-replacement
if (import.meta.hot) {
  import.meta.hot.accept();
}
