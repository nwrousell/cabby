import { Box, Flex, Heading } from '@chakra-ui/react';

const Header = () => {
  return (
    <Flex
      as="header"
      width="full"
      align="center"
      alignSelf="flex-start"
      justifyContent="center"
      gridGap={2}
    >
      <Box>
        <Heading>Cabby</Heading>
      </Box>
    </Flex>
  );
};

export default Header;
