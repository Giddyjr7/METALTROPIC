
import React from 'react';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger
} from "@/components/ui/accordion";

import { faqItems } from '../data/faqData';

const FAQ = () => {
  return (
    <section id="faq" className="py-24 bg-gradient-to-b from-[#12141C] to-crypto-blue">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-gradient">
            Frequently Asked Questions
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Got questions about MetalTropic? We've got answers. If you don't see what you're looking for, reach out to our support team.
          </p>
        </div>

        <div className="max-w-3xl mx-auto">
          <Accordion type="single" collapsible className="space-y-4">
            {faqItems.map((item, index) => (
              <AccordionItem 
                key={index} 
                value={`item-${index}`}
                className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl overflow-hidden animate-on-scroll"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <AccordionTrigger className="px-6 py-4 text-white hover:text-crypto-purple hover:no-underline">
                  {item.question}
                </AccordionTrigger>
                <AccordionContent className="px-6 pb-4 text-gray-400">
                  {item.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </section>
  );
};

export default FAQ;
