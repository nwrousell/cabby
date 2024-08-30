import { extendTheme } from '@chakra-ui/react';

export const theme = extendTheme({
  fonts: {
    heading: 'Plus Jakarta Sans, sans-serif',
    body: 'Plus Jakarta Sans, sans-serif',
  },
  components: {
    // Button: {
    // }
  },
  config: {
    initialColorMode: 'dark',
    useSystemColorMode: false,
  },
  colors: {
    brand: {
      900: '#1a365d',
      800: '#153e75',
      700: '#2a69ac',
    },
  },
  styles: {
    global: {
      body: {
        bg: 'brand.900',
        color: 'white',
      },
    },
  },
});
