import { Box, Heading, Stack, StackDivider, VStack } from '@chakra-ui/react';
import React from 'react';
import CoordDisplay from '../components/coordinates/CoordDisplay';
import Form from '../components/form/Form';
import GetFares from '../components/GetFares';

const Hero = () => {
  return (
    <Box
      mt="-150px"
      px={{ base: 8, lg: 10 }}
      py={6}
      boxShadow="lg"
      bgColor="white"
      borderRadius={15}
    >
      <Heading as="h1">Uber Fares ML Demo</Heading>
      <Stack
        direction={{ base: 'column', lg: 'row' }}
        divider={<StackDivider borderColor="gray.200" />}
        spacing={8}
        align="stretch"
        width="100%"
        pt={{ base: 4, lg: 6 }}
      >
        <Box flexGrow={1} flexBasis={0} boxSizing="border-box">
          <VStack spacing={4}>
            <Form />
          </VStack>
        </Box>
        <Box flexGrow={1} flexBasis={0} boxSizing="border-box">
          <Stack
            justifyContent={{ base: 'space-between', lg: 'flex-start' }}
            direction={{ base: 'column', md: 'row', lg: 'column' }}
            spacing={4}
          >
            <CoordDisplay />
          </Stack>
        </Box>
        <Box flexGrow={1} flexBasis={0} boxSizing="border-box">
          <GetFares />
        </Box>
      </Stack>
    </Box>
  );
};

export default Hero;
