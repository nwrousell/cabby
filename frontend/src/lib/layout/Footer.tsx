import { Flex, Link, Text } from '@chakra-ui/react';

const Footer = () => {
    return (
        <Flex
            as="footer"
            width="full"
            align="center"
            alignSelf="flex-end"
            justifyContent="center"
            flex={0}
        >
            <Text fontSize="xs">
                {new Date().getFullYear()} -{' '}
                <Link href="https://sznm.dev" isExternal>
                    cabby
                </Link>
            </Text>
        </Flex>
    );
};

export default Footer;
