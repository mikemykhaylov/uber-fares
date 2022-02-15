import React from 'react';
import { FormControl, FormHelperText, FormLabel } from '@chakra-ui/react';
import PassengerCount from './PassengerCount';
import YearSelector from './YearSelector';

const Form = () => {
  return (
    <>
      <FormControl isRequired>
        <FormLabel htmlFor="passengerCount">Passenger Count</FormLabel>
        <PassengerCount />
      </FormControl>
      <FormControl isRequired>
        <FormLabel htmlFor="year">Year</FormLabel>
        <YearSelector />
        <FormHelperText>That&apos;s the year we&apos;ll compare to current prices</FormHelperText>
      </FormControl>
    </>
  );
};

export default Form;
