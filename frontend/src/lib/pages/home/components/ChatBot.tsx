import { useState } from 'react';
import {
  Box,
  VStack,
  Input,
  Text,
  Flex,
  IconButton,
  Spinner,
} from '@chakra-ui/react';
import { IoSend } from 'react-icons/io5';

const ChatMessage = ({ message, isUser, isLoading = false }) => (
  <Box
    bg={isUser ? 'brand.700' : 'brand.800'}
    color="white"
    p={3}
    borderRadius="lg"
    maxW="70%"
    alignSelf={isUser ? 'flex-end' : 'flex-start'}
    mb={2}
  >
    {isLoading ? <Spinner mx="36" my="3" /> : <Text>{message}</Text>}
  </Box>
);

type Message = {
  text: string;
  role: 'user' | 'assistant';
};

export default function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      text: "Hello, I'm Cabby! You can talk to me about courses at Brown. I have access to CAB, Critical Review (and Bulletin soon). What can I help you with today?",
      role: 'user',
    },
  ]);

  const [input, setInput] = useState('');
  const [waitingOnResponse, setWaitingOnResponse] = useState(false);

  const handleSend = () => {
    if (!waitingOnResponse && input.trim()) {
      setMessages([...messages, { text: input, role: 'user' }]);

      setWaitingOnResponse(true);
      setTimeout(() => {
        setMessages((msgs) => [...msgs, { text: 'hi.', role: 'assistant' }]);
        setWaitingOnResponse(false);
      }, 3000);

      setInput('');
    }
  };

  return (
    <Box display="flex" flex={1} flexDirection="column" overflowY="hidden">
      <VStack
        flex={'1'}
        spacing={4}
        p={4}
        overflowY="scroll"
        sx={{
          '::-webkit-scrollbar': {
            display: 'none',
          },
        }}
      >
        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            message={message.text}
            isUser={message.role == 'user'}
          />
        ))}

        {waitingOnResponse && (
          <ChatMessage message={''} isUser={false} isLoading />
        )}
      </VStack>

      <Flex p={4} flex={0} bg="brand.800" borderRadius={'6'}>
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          mr={2}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <IconButton
          onClick={handleSend}
          disabled={waitingOnResponse}
          colorScheme={waitingOnResponse ? 'gray' : 'blue'}
          icon={<IoSend />}
          aria-label={'Send Button'}
        />
      </Flex>
    </Box>
  );
}
