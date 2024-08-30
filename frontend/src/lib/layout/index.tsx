import { Box, Flex } from '@chakra-ui/react';
import type { ReactNode } from 'react';

import Footer from './Footer';
import Header from './Header';
import Meta from './Meta';

type LayoutProps = {
    children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
    return (
        <Box margin="0 auto" maxWidth={800} transition="0.5s ease-out">
            <Meta />
            <Flex margin="4" h="95vh" flexDir={'column'} justifyContent={'start'}>
                <Header />
                <Flex flexDir={'column'} flex={1} overflowY={'hidden'}>
                    {children}
                </Flex>
                <Footer />
            </Flex>
        </Box>
    );
};

export default Layout;
