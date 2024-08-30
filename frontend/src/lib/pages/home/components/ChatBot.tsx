import { useState } from 'react';
import { Box, VStack, Input, Text, Flex, IconButton } from '@chakra-ui/react';
import { IoSend } from "react-icons/io5";

const ChatMessage = ({ message, isUser }) => (
    <Box
        bg={isUser ? 'brand.700' : 'brand.800'}
        color="white"
        p={3}
        borderRadius="lg"
        maxW="70%"
        alignSelf={isUser ? 'flex-end' : 'flex-start'}
        mb={2}
    >
        <Text>{message}</Text>
    </Box>
)

export default function ChatBot() {
    const [messages, setMessages] = useState([
        { text: "Hello! I'm your colorful chatbot. How can I brighten your day?", isUser: false },
    ]);
    const [input, setInput] = useState('');

    const handleSend = () => {
        if (input.trim()) {
            setMessages([...messages, { text: input, isUser: true }]);
            // Simulated bot response
            setTimeout(() => {
                setMessages(prev => [...prev, {
                    text: `Thanks for your message: "${input}"! I'm just a demo, but I'm here to make your UI colorful!`,
                    isUser: false
                }]);
            }, 1000);
            setInput('')
        }
    }

    return (
        <Box display="flex" flex={1} flexDirection="column" overflowY='hidden'>
            <VStack 
                flex={'1'} 
                spacing={4} 
                p={4} 
                overflowY="scroll"
                sx={{
                    "::-webkit-scrollbar": {
                        display: "none",
                    },
                }}
            >
                {messages.map((message, index) => (
                    <ChatMessage key={index} message={message.text} isUser={message.isUser} />
                ))}
            </VStack>

            <Flex p={4} flex={0} bg="brand.800">
                <Input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type a message..."
                    mr={2}
                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                />
                <IconButton
                    onClick={handleSend}
                    colorScheme='blue'
                    icon={<IoSend />} 
                    aria-label={'Send Button'}                
                />
            </Flex>
        </Box>
    );
}