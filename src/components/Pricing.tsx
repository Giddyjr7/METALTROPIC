// Pricing.tsx

import { Button } from '@/components/ui/button';
import { Check } from 'lucide-react';
import { pricingPlans } from '@/data/pricingData'; // adjust path if necessary

const Pricing = () => {
  return (
    <section id="pricing" className="py-24 bg-[#12141C]">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-gradient">
            Simple, Transparent Plans
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto mb-8">
            Choose the investment plan that best fits your financial goals. All plans include secure fund management and compound interest options.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {pricingPlans.map((plan, index) => (
            <div 
              key={index} 
              className={`bg-white/5 backdrop-blur-sm border rounded-xl overflow-hidden animate-on-scroll ${
                plan.highlighted 
                  ? 'border-crypto-purple relative shadow-xl shadow-crypto-purple/10' 
                  : 'border-white/10'
              }`}
              style={{ animationDelay: `${index * 0.2}s` }}
            >
              {plan.highlighted && (
                <div className="bg-crypto-purple text-white text-center py-1 text-sm font-medium">
                  Most Popular
                </div>
              )}
              <div className="p-8">
                <h3 className="text-xl font-semibold mb-2 text-white">{plan.name}</h3>
                <p className="text-gray-400 mb-6">{plan.description}</p>
                
                <Button 
                  className={`w-full mb-6 ${
                    plan.highlighted 
                      ? 'bg-crypto-purple hover:bg-crypto-dark-purple' 
                      : 'bg-white/10 hover:bg-white/20 text-white'
                  }`}
                >
                  {plan.buttonText}
                </Button>
                
                <div>
                  <p className="text-sm font-medium text-gray-300 mb-4">Plan Details:</p>
                  <ul className="space-y-3">
                    {plan.features.map((feature, i) => (
                      <li key={i} className="flex items-start">
                        <Check className="h-5 w-5 text-crypto-purple mr-3 shrink-0" />
                        <span className="text-gray-400 text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Pricing;
