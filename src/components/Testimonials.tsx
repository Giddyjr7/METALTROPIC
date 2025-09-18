import { useState, useEffect, useRef } from 'react';
import { Star } from 'lucide-react';
import { testimonials } from '../data/testimonials';

const Testimonials = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState(true);
  const autoPlayRef = useRef<NodeJS.Timeout | null>(null);

  const nextSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % testimonials.length);
  };

  const goToSlide = (index: number) => {
    setCurrentIndex(index);
  };

  useEffect(() => {
    if (isAutoPlaying) {
      autoPlayRef.current = setInterval(() => {
        nextSlide();
      }, 5000);
    }
    
    return () => {
      if (autoPlayRef.current) {
        clearInterval(autoPlayRef.current);
      }
    };
  }, [isAutoPlaying]);

  const handleMouseEnter = () => {
    setIsAutoPlaying(false);
  };

  const handleMouseLeave = () => {
    setIsAutoPlaying(true);
  };

  return (
    <section id="testimonials" className="py-24 bg-gradient-to-b from-crypto-blue to-[#12141C]">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-gradient">
            What Our Users Say
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Join thousands of satisfied traders who have transformed their trading experience with MetalTropic.
          </p>
        </div>

        <div 
          className="relative max-w-4xl mx-auto"
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
        >
          <div className="overflow-hidden">
            <div 
              className="flex transition-transform duration-500 ease-out" 
              style={{ transform: `translateX(-${currentIndex * 100}%)` }}
            >
              {testimonials.map((testimonial, index) => (
                <div key={index} className="min-w-full px-4">
                  <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-8 md:p-10">
                    <div className="flex mb-6">
                      {[...Array(5)].map((_, i) => (
                        <Star key={i} className="h-5 w-5 text-yellow-500 fill-yellow-500" />
                      ))}
                    </div>
                    <p className="text-lg md:text-xl text-gray-200 mb-8">"{testimonial.quote}"</p>
                    <div className="flex items-center">
                      <img 
                        src={testimonial.avatar} 
                        alt={testimonial.author} 
                        className="w-12 h-12 rounded-full object-cover border-2 border-crypto-purple"
                      />
                      <div className="ml-4">
                        <p className="font-medium text-white">{testimonial.author}</p>
                        <p className="text-sm text-gray-400">{testimonial.role}</p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* No prev/next buttons */}
          <div className="flex justify-center mt-6 space-x-2">
            {testimonials.map((_, index) => (
              <button
                key={index}
                onClick={() => goToSlide(index)}
                className={`h-2 rounded-full transition-all duration-300 ${currentIndex === index ? 'w-8 bg-crypto-purple' : 'w-2 bg-gray-500'}`}
                aria-label={`Go to testimonial ${index + 1}`}
              ></button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
